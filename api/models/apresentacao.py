from django.db import models, transaction

from api.models.configuracao import Configuracao
from api.models.produto import Produto
from api.models.unidade import Unidade


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


class Apresentacao(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True, unique=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    registro_ms = models.CharField(max_length=17, null=True, blank=True)
    produto = models.ForeignKey(Produto, related_name='apresentacoes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    ativo = models.BooleanField(default=True)
    unidade = models.ForeignKey(Unidade, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    classe_terapeutica = models.CharField(max_length=254, null=True, blank=True)
    ranking_visualizacao = models.BigIntegerField(default=0)
    ranking_proposta = models.BigIntegerField(default=0)
    ranking_compra = models.BigIntegerField(default=0)
    objects = ApresentacaoManager()

    def __str__(self):
        return self.nome if self.nome else self.produto.nome

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
