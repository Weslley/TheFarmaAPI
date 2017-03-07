from rest_framework import serializers
from api.models.produto import Produto
from api.serializers.apresentacao import ApresentacaoListSerializer


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
