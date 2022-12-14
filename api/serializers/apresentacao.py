import locale
from decimal import Decimal

from django.contrib.sites.models import Site
from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer
from api.models.ultimo_preco import UltimoPreco
from api.models.apresentacao import Apresentacao, ImagemApresentacao
from api.models.estoque import Estoque
from api.models.produto import Produto
from api.models.uf import Uf
from api.serializers.principio_ativo import PrincipioAtivoBasicSerializer
from api.serializers.tabela_preco import TabelaPrecoSerializer
from django.conf import settings
from django.db.models import Avg


class ApresentacaoSerializer(serializers.ModelSerializer):
    tabelas = TabelaPrecoSerializer(many=True)

    class Meta:
        model = Apresentacao
        fields = ('codigo_barras', 'nome', 'registro_ms', 'tabelas', 'ativo')


class ApresentacaoExportSerializer(serializers.ModelSerializer):
    tabelas = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class ImagemApresentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemApresentacao
        fields = ('imagem', )


class ApresentacaoBusca(serializers.ModelSerializer):
    preco = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    pmc = serializers.SerializerMethodField()
    data_atualizacao = serializers.SerializerMethodField()
    nome = serializers.SerializerMethodField()
    embalagem = serializers.SerializerMethodField()
    forma_farmaceutica = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = (
            'id',
            'codigo_barras',
            'nome',
            'embalagem',
            'forma_farmaceutica',
            'preco',
            'imagens',
            'imagem',
            'pmc',
            'data_atualizacao',
        )

    def get_nome(self, obj):
        return obj.nome_apresentacao
    
    def get_embalagem(self, obj):
        if obj.embalagem:
            return obj.embalagem.tipo
    
    def get_forma_farmaceutica(self, obj):
        if obj.forma_farmaceutica:
            return obj.forma_farmaceutica.nome

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)

    def get_pmc(self, obj):
        pmc = Decimal(0)

        try:
            uf = Uf.objects.get(sigla=self.context['view'].kwargs['uf'])
            tabela = obj.tabelas.get(icms=uf.icms)
            pmc = tabela.pmc
        except Exception as err:
            pass

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        pmc = locale.currency(pmc, grouping=True, symbol=None)

        return pmc

    def get_preco(self, obj):
        cidade = self.context['cidade']
        preco = Decimal(0)

        estoque = Estoque.objects.filter(
            apresentacao=obj,
            farmacia__endereco__cidade=cidade
        ).order_by('valor').first()
        if estoque:
            preco = estoque.valor

        return round(preco, 2)

    def get_imagem(self, obj):
        return obj.imagem_url


class ProdutoFabricante(serializers.ModelSerializer):
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = PrincipioAtivoBasicSerializer()
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'principio_ativo', 'tipo', 'tipo_venda')


class ProdutoSimplesSerializer(serializers.ModelSerializer):
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = serializers.CharField(read_only=True, source='principio_ativo.nome')
    tipo_venda = serializers.IntegerField(read_only=True, source='principio_ativo.tipo_venda')

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'principio_ativo', 'tipo', 'tipo_venda')


class ProdutoCompletoSerializer(ProdutoSimplesSerializer):
    secao = serializers.CharField(read_only=True, source='secao.nome')
    subsecao = serializers.CharField(read_only=True, source='subsecao.nome')
    sintomas = serializers.StringRelatedField(many=True)

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'descricao', 'principio_ativo', 'tipo', 'secao', 'subsecao', 'sintomas')


class ApresentacaoBuscaProduto(serializers.ModelSerializer):
    preco = serializers.SerializerMethodField()
    pmc = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    #unidade = serializers.CharField(source='unidade.nome')
    produto = ProdutoFabricante()
    nome = serializers.SerializerMethodField()
    embalagem = serializers.SerializerMethodField()
    forma_farmaceutica = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = (
            'id',
            'codigo_barras',
            'nome',
            'embalagem',
            'forma_farmaceutica',
            'preco',
            'imagem',
            'produto',
            'pmc',
            'quantidade',
        )

    def get_nome(self, obj):
        return obj.nome_apresentacao

    def get_embalagem(self, obj):
        if obj.embalagem:
            return obj.embalagem.tipo
    
    def get_forma_farmaceutica(self, obj):
        if obj.forma_farmaceutica:
            return obj.forma_farmaceutica.nome

    def get_preco(self, obj):
        cidade = self.context['cidade']
        preco = Decimal(0)

        estoque = Estoque.objects.filter(
            apresentacao=obj,
            farmacia__endereco__cidade=cidade
        ).order_by('valor').first()
        if estoque:
            preco = estoque.valor
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        preco = locale.currency(preco, grouping=True, symbol=None)
        return preco

    def get_pmc(self, obj):
        cidade = self.context['cidade']
        pmc = Decimal(0)

        try:
            tabela = obj.tabelas.get(icms=cidade.uf.icms)
            pmc = tabela.pmc
        except Exception as err:
            pass
        #calcula preco medio dos ultimos 100
        if (pmc == 0):
            try:
                ultimo_preco = UltimoPreco.objects.values('id','valor')\
                                            .filter(apresentacao_id=obj.id)[:100]\
                                            .aggregate(Avg('valor'))
                pmc = ultimo_preco['valor__avg'] if ultimo_preco['valor__avg'] else 0
            except Exception as err:
                pass

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        pmc = locale.currency(pmc, grouping=True, symbol=None)

        return pmc

    def get_imagem(self, obj):
        return obj.imagem_url



class ApresentacaoProdutoRetrieve(ApresentacaoBuscaProduto):
    produto = ProdutoCompletoSerializer()


class ApresentacaoListSerializer(serializers.ModelSerializer):
    produto = ProdutoSimplesSerializer()
    pmc = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'imagem', 'produto', 'pmc', 'codigo_barras')

    def get_pmc(self, obj):
        cidade = self.context['cidade'] if 'cidade' in self.context else None
        pmc = Decimal(0)

        try:
            tabela = obj.tabelas.get(icms=cidade.uf.icms)
            pmc = tabela.pmc
        except Exception as err:
            pass

        return float(pmc)

    def get_imagem(self, obj):
        return obj.imagem_url
