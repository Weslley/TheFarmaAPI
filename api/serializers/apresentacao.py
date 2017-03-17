from rest_framework import serializers
from api.models.apresentacao import Apresentacao
from api.models.estoque import Estoque
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
        fields = ('codigo_barras', 'nome', 'registro_ms', 'imagem', 'tabelas', 'ativo')


class ApresentacaoExportSerializer(serializers.ModelSerializer):
    tabelas = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class ApresentacaoBusca(serializers.ModelSerializer):
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'preco')

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
