from django.db import models, transaction

from versatileimagefield.fields import VersatileImageField, PPOIField

from api.models.configuracao import Configuracao
from api.models.produto import Produto
from api.models.unidade import Unidade

import locale

EXECOES = [
    'Comprimidos',
    'Cápsula',
    'Pílula',
    'Pastilha',
    'Comprimido efervescente',
    'Comprimido revestido',
    'Cápsulas moles',
    'Comprimido mastigável',
    'Comprimido liberação prolongada',
    'Cápsula gel mole',
    'Comprimido sublingual'
]


class ApresentacaoManager(models.Manager):

    def update_ranking_visualizacao(self, id):
        """
        Metodo para atualizar o ranking de visualização da apresentação
        :param id: Id da apresentacao
        :return:
        """
        try:
            with transaction.atomic():
                apresentacao = self.get(id=id)
                apresentacao.ranking_visualizacao += 1
                apresentacao.save()
        except Exception as e:
            print(e)

    def update_ranking_proposta(self, id):
        """
        Metodo para atualizar o ranking de proposta da apresentação
        :param id: Id da apresentacao
        :return:
        """
        try:
            with transaction.atomic():
                apresentacao = self.get(id=id)
                apresentacao.ranking_proposta += 1
                apresentacao.save()
        except Exception as e:
            print(e)

    def update_ranking_compra(self, id):
        """
        Metodo para atualizar o ranking de compra da apresentação
        :param id: Id da apresentacao
        :return:
        """
        try:
            with transaction.atomic():
                apresentacao = self.get(id=id)
                apresentacao.ranking_compra += 1
                apresentacao.save()
        except Exception as e:
            print(e)


class FormaFarmaceutica(models.Model):
    nome = models.CharField(max_length=75)

    def __str__(self):
        return self.nome


class Embalagem(models.Model):
    tipo = models.CharField(max_length=75)

    def __str__(self):
        return self.tipo


class Sufixo(models.Model):
    nome = models.CharField(max_length=75)

    def __str__(self):
        return self.nome


def generate_apresentacao_filename(self, filename):
    return 'apresentacoes/{0}/{1}'.format(str(self.codigo_barras).zfill(14), filename)


class Apresentacao(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True, unique=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    registro_ms = models.CharField(max_length=17, null=True, blank=True)
    produto = models.ForeignKey(Produto, related_name='apresentacoes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now=True)
    ativo = models.BooleanField(default=True)
    unidade = models.ForeignKey(Unidade, null=True, blank=True)
    classe_terapeutica = models.CharField(max_length=254, null=True, blank=True)
    ranking_visualizacao = models.BigIntegerField(default=0)
    ranking_proposta = models.BigIntegerField(default=0)
    ranking_compra = models.BigIntegerField(default=0)
    patrocinio = models.BigIntegerField(default=0)

    imagem = VersatileImageField(
        upload_to=generate_apresentacao_filename,
        ppoi_field='apresentacao_ppoi',
        null=True, blank=True
    )
    apresentacao_ppoi = PPOIField()

    forma_farmaceutica = models.ForeignKey(
        FormaFarmaceutica, related_name='apresentacoes',
        null=True
    )
    embalagem = models.ForeignKey(
        Embalagem, related_name='apresentacoes', null=True, blank=True
    )
    dosagem = models.DecimalField(
        null=True, max_digits=15, decimal_places=3, blank=True
    )
    sufixo_dosagem = models.ForeignKey(
        Sufixo, related_name='apresentacoes_com_sufixo_dosagem',
        null=True, verbose_name='Sufixo da Dosagem', blank=True
    )

    segunda_dosagem = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=3
    )
    sufixo_segunda_dosagem = models.ForeignKey(
        Sufixo, related_name='apresentacoes_com_sufixo_segunda_dosagem',
        null=True, blank=True, verbose_name='Sufixo da Segunda Dosagem'
    )
    terceira_dosagem = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=3
    )
    sufixo_terceira_dosagem = models.ForeignKey(
        Sufixo, related_name='apresentacoes_com_sufixo_teceira_dosagem',
        null=True, blank=True, verbose_name='Sufixo da Terceira Dosagem'
    )

    quarta_dosagem = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=3
    )

    sufixo_quarta_dosagem = models.ForeignKey(
        Sufixo, related_name='apresentacoes_com_sufixo_quarta_dosagem',
        null=True, blank=True, verbose_name='Sufixo da Quarta Dosagem'
    )

    quantidade = models.DecimalField(
        null=True, max_digits=15, decimal_places=2
    )
    sufixo_quantidade = models.ForeignKey(
        Sufixo, related_name='apresentacoes_com_sufixo_quantidade',
        blank=True, null=True, verbose_name='Sufixo da Quantidade',
        help_text="Não obrigatório"
    )

    comercializado = models.BooleanField(default=True)
    pbm = models.BooleanField(default=False)
    identificado = models.BooleanField(default=False)
    data_atualizacao_manual = models.DateTimeField(blank=True,null=True)

    objects = ApresentacaoManager()

    def __str__(self):
        return self.nome if self.nome else self.produto.nome

    @property
    def nome_apresentacao(self):
        """ try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            
            def clean_decimal(decimal_value):
                dc_tuple = decimal_value.as_tuple()
                exp_tuple = dc_tuple.digits[dc_tuple.exponent:]
                if max(exp_tuple) == 0:
                    return int(
                        ''.join(
                            [str(_) for _ in dc_tuple.digits[:dc_tuple.exponent]]
                        )
                    )
                return locale.currency(decimal_value, grouping=True, symbol=None)

            if not self.identificado:
                return self.nome

            default_decimal_fields = ['dosagem', 'quantidade']
            extra_decimal_fields = ['segunda_dosagem', 'terceira_dosagem']
            fmt_values = {
                df_field:clean_decimal(getattr(self, df_field))
                for df_field in default_decimal_fields
            }

            extra = []
            for extra_field in extra_decimal_fields:
                result = getattr(self, extra_field)
                if result:
                    fmt_values[extra_field] = clean_decimal(result)
                    extra.append(extra_field)

            dosagem = fmt_values.get('dosagem')
            quantidade = fmt_values.get('quantidade')
            if extra:
                segunda_dosagem = fmt_values.get('segunda_dosagem', None)
                terceira_dosagem = fmt_values.get('terceira_dosagem', None)
                prefixo_apresentacao = '{}{}'.format(dosagem, self.sufixo_dosagem)

                if segunda_dosagem:
                    prefixo_apresentacao += '+{}{}'.format(
                        segunda_dosagem, self.sufixo_segunda_dosagem
                    )
                if terceira_dosagem:
                    prefixo_apresentacao += '+{}{}'.format(
                        terceira_dosagem, self.sufixo_terceira_dosagem
                    )

            else:
                prefixo_apresentacao = '{}{}'.format(dosagem, self.sufixo_dosagem)

            if self.sufixo_quantidade:
                final_apresentacao = ", {} com {}{}".format(
                    self.forma_farmaceutica.nome, quantidade,
                    self.sufixo_quantidade
                )
            elif self.forma_farmaceutica.nome in ['Comprimidos','Cápsula','Pílula','Pastilha','Comprimido efervescente','Comprimido revestido','Cápsulas moles','Comprimido mastigável','Comprimido liberação prolongada','Cápsula gel mole','Comprimido sublingual'] :
                final_apresentacao = ", {} {}".format(
                    quantidade, self.forma_farmaceutica.nome.lower()
                )
            else:
                final_apresentacao = ", {} {}".format(
                    quantidade, self.forma_farmaceutica.nome.lower()
                )

            return prefixo_apresentacao + final_apresentacao
        except Exception as err:
            print(str(err))
            return self.nome """
        try:
            #formata o nome
            nome = ''
            virgula = False #caso tenha dosagem sera necessario uma virgula
            #se nao esta identificado retorna o nome
            if not self.identificado:
                return self.nome
            #verifica se tem dosagem
            if self.dosagem:
                virgula = True
                dosagem = locale.currency(self.dosagem, symbol=False)
                nome += '{} {}'.format(dosagem,self.sufixo_dosagem.nome)
            if self.segunda_dosagem:
                dosagem = locale.currency(self.segunda_dosagem, symbol=False)
                nome += ' + {} {}'.format(dosagem,self.sufixo_segunda_dosagem)
            if self.terceira_dosagem:
                dosagem = locale.currency(self.terceira_dosagem, symbol=False)
                nome += ' + {} {}'.format(dosagem,self.sufixo_terceira_dosagem.nome)
            if self.quarta_dosagem:
                dosagem = locale.currency(self.quarta_dosagem, symbol=False)
                nome += ' + {} {}'.format(dosagem,self.sufixo_quarta_dosagem.nome)
            #se  tiver dosagem precisa da virgula
            if virgula:
                nome += ','
            #verifica se a forma farmaceutica eh uma excecao
            if self.forma_farmaceutica.nome in EXECOES:
                nome += ' {} {}'.format(self.quantidade,self.forma_farmaceutica.nome)
            else:
                nome += '{} com {}'.format(self.forma_farmaceutica.nome,self.quantidade)
            if self.sufixo_quantidade:
                nome += ' {}'.format(self.sufixo_quantidade.nome)
            return nome
        except Exception as err:
            print(str(err))
            return self.nome

    @property
    def ranking(self):
        configuracao = Configuracao.objects.first()
        return (self.ranking_visualizacao * configuracao.peso_ranking_visualizacao) + \
               (self.ranking_proposta * configuracao.peso_ranking_proposta) + \
               (self.ranking_compra * configuracao.peso_ranking_compra)

    @property
    def get_manager(self):
        return self.__class__.objects


def generate_filename(self, filename):
    return 'apresentacoes/{0}/{1}'.format(self.apresentacao_id, filename)


class ImagemApresentacao(models.Model):
    imagem = models.ImageField(upload_to=generate_filename, null=True, blank=True)
    capa = models.BooleanField(default=False)
    apresentacao = models.ForeignKey(Apresentacao, related_name='imagens')
