import locale
from decimal import Decimal

from django.contrib.sites.models import Site
from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from api.models.apresentacao import Apresentacao, ImagemApresentacao
from api.models.estoque import Estoque
from api.models.produto import Produto
from api.models.uf import Uf
from api.serializers.principio_ativo import PrincipioAtivoBasicSerializer
from api.serializers.tabela_preco import TabelaPrecoSerializer
from django.conf import settings


class ApresentacaoSerializer(serializers.ModelSerializer):
    tabelas = TabelaPrecoSerializer(many=True)

    class Meta:
        model = Apresentacao
        fields = ('codigo_barras', 'nome', 'registro_ms', 'tabelas', 'ativo', 'classe_terapeutica')


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
    imagens = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    unidade = serializers.CharField(source='unidade.nome')
    pmc = serializers.SerializerMethodField()
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = (
            'id',
            'codigo_barras',
            'nome',
            'preco',
            'imagens',
            'unidade',
            'imagem',
            'pmc',
            'data_atualizacao',
            'classe_terapeutica'
        )

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
        qs = obj.imagens.order_by('-capa').first()
        serializer = ImagemApresentacaoSerializer(instance=qs, context=self.context)
        data = serializer.data['imagem']

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data = request.build_absolute_uri(obj.unidade.imagem.url)

        return data

    def get_imagens(self, obj):
        qs = obj.imagens.order_by('-capa')
        serializer = ImagemApresentacaoSerializer(instance=qs, many=True, context=self.context)
        data = [_['imagem'] for _ in serializer.data]

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data.append(request.build_absolute_uri(obj.unidade.imagem.url))

        return data


class ProdutoFabricante(serializers.ModelSerializer):
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = PrincipioAtivoBasicSerializer()

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'tipo', 'principio_ativo')


class ProdutoSimplesSerializer(serializers.ModelSerializer):
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = serializers.CharField(read_only=True, source='principio_ativo.nome')

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'principio_ativo', 'tipo')


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
    # imagens = serializers.SerializerMethodField()
    imagem = VersatileImageFieldSerializer(
        sizes=[
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
        ]
    )
    unidade = serializers.CharField(source='unidade.nome')
    produto = ProdutoFabricante()

    class Meta:
        model = Apresentacao
        fields = (
            'id',
            'codigo_barras',
            'nome',
            'preco',
            # 'imagens',
            'unidade',
            'produto',
            'imagem',
            'pmc',
            'quantidade',
            'classe_terapeutica'
        )

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

    # def get_imagens(self, obj):
    #     qs = obj.imagens.order_by('-capa')
    #     serializer = ImagemApresentacaoSerializer(instance=qs, many=True, context=self.context)
    #     data = [_['imagem'] for _ in serializer.data]

    #     # verificando se tem um tipo caso não possua imagens
    #     if not data and obj.unidade:
    #         request = self.context['request']
    #         data.append(request.build_absolute_uri(obj.unidade.imagem.url))

    #     return data

    def get_imagem(self, obj):
        qs = obj.imagens.order_by('-capa').first()
        serializer = ImagemApresentacaoSerializer(instance=qs, context=self.context)
        data = serializer.data['imagem']

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data = request.build_absolute_uri(obj.unidade.imagem.url)

        return data

    def get_pmc(self, obj):
        cidade = self.context['cidade']
        pmc = Decimal(0)

        try:
            tabela = obj.tabelas.get(icms=cidade.uf.icms)
            pmc = tabela.pmc
        except Exception as err:
            pass

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        pmc = locale.currency(pmc, grouping=True, symbol=None)

        return pmc


class ApresentacaoProdutoRetrieve(ApresentacaoBuscaProduto):
    produto = ProdutoCompletoSerializer()


class ApresentacaoListSerializer(serializers.ModelSerializer):
    imagem = serializers.SerializerMethodField()
    unidade = serializers.CharField(source='unidade.nome')
    produto = ProdutoSimplesSerializer()
    pmc = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = ('nome', 'id', 'imagem', 'unidade', 'produto', 'pmc', 'classe_terapeutica', 'codigo_barras')

    def get_imagem(self, obj):
        qs = obj.imagens.order_by('-capa').first()
        serializer = ImagemApresentacaoSerializer(instance=qs, context=self.context)
        data = serializer.data['imagem']

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            if 'request' in self.context:
                request = self.context['request']
                return request.build_absolute_uri(obj.unidade.imagem.url) if obj.unidade.imagem.url else None
            else:
                return '{}{}/{}/'.format(
                    settings.HTTPS,
                    Site.objects.get_current().domain,
                    obj.unidade.imagem.url
                )
        elif data:
            return '{}{}{}'.format(
                settings.HTTPS,
                Site.objects.get_current().domain,
                data
            )
        else:
            return None

    def get_pmc(self, obj):
        cidade = self.context['cidade'] if 'cidade' in self.context else None
        pmc = Decimal(0)

        try:
            tabela = obj.tabelas.get(icms=cidade.uf.icms)
            pmc = tabela.pmc
        except Exception as err:
            pass

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        pmc = locale.currency(pmc, grouping=True, symbol=None)

        return pmc
