from rest_framework import serializers
from api.models.produto import Produto
from api.serializers.apresentacao import ApresentacaoListSerializer, ApresentacaoBusca
from api.serializers.principio_ativo import PrincipioAtivoBasicSerializer


class MedicamentoSerializer(serializers.ModelSerializer):
    apresentacoes = ApresentacaoListSerializer(many=True)
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class MedicamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('nome', 'id')


class MedicamentoExportSerializer(serializers.ModelSerializer):
    apresentacoes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class ProdutoSerializer(serializers.ModelSerializer):
    apresentacoes = serializers.SerializerMethodField()
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = PrincipioAtivoBasicSerializer()

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'fabricante', 'apresentacoes', 'principio_ativo')

    def get_apresentacoes(self, obj):
        qs = obj.apresentacoes.filter(ativo=True)
        serializer = ApresentacaoBusca(instance=qs, many=True, context=self.context)
        return serializer.data
