from rest_framework import serializers
from api.models.apresentacao import Apresentacao, ImagemApresentacao
from api.models.estoque import Estoque
from api.models.produto import Produto
from api.serializers.tabela_preco import TabelaPrecoSerializer
from decimal import Decimal


class ApresentacaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apresentacao
        fields = ('nome', 'id')


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
    unidade = serializers.CharField(source='unidade.nome')

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'preco', 'imagens', 'unidade')

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


class ApresentacaoBuscaProduto(serializers.ModelSerializer):
    preco = serializers.SerializerMethodField()
    imagens = serializers.SerializerMethodField()
    unidade = serializers.CharField(source='unidade.nome')
    produto = ProdutoFabricante()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'preco', 'imagens', 'unidade', 'produto')

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

    def get_imagens(self, obj):
        qs = obj.imagens.order_by('-capa')
        serializer = ImagemApresentacaoSerializer(instance=qs, many=True, context=self.context)
        data = [_['imagem'] for _ in serializer.data]

        # verificando se tem um tipo caso não possua imagens
        if not data and obj.unidade:
            request = self.context['request']
            data.append(request.build_absolute_uri(obj.unidade.imagem.url))

        return data
