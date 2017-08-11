import locale
from decimal import Decimal

from rest_framework import serializers

from api.models.apresentacao import Apresentacao, ImagemApresentacao
from api.models.estoque import Estoque
from api.models.produto import Produto
from api.models.uf import Uf
from api.serializers.tabela_preco import TabelaPrecoSerializer


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
    imagens = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    unidade = serializers.CharField(source='unidade.nome')
    pmc = serializers.SerializerMethodField()
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'preco', 'imagens', 'unidade', 'imagem', 'pmc', 'data_atualizacao')

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

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante')


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
    imagens = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    unidade = serializers.CharField(source='unidade.nome')
    produto = ProdutoFabricante()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'preco', 'imagens', 'unidade', 'produto', 'imagem', 'pmc', 'quantidade')

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

    def get_imagens(self, obj):
        qs = obj.imagens.order_by('-capa')
        serializer = ImagemApresentacaoSerializer(instance=qs, many=True, context=self.context)
        data = [_['imagem'] for _ in serializer.data]

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data.append(request.build_absolute_uri(obj.unidade.imagem.url))

        return data

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

    class Meta:
        model = Apresentacao
        fields = ('nome', 'id', 'imagem', 'unidade', 'produto')

    def get_imagem(self, obj):
        qs = obj.imagens.order_by('-capa').first()
        serializer = ImagemApresentacaoSerializer(instance=qs, context=self.context)
        data = serializer.data['imagem']

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data = request.build_absolute_uri(obj.unidade.imagem.url)

        return data
