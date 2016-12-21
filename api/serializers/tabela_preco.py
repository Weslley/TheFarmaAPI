from rest_framework import serializers
from api.models.tabela_preco import TabelaPreco
from api.serializers.uf import UfReduzidoSerializer


class TabelaPrecoSerializer(serializers.ModelSerializer):
    ufs = serializers.SlugRelatedField(many=True, read_only=True, slug_field='sigla')
    data_atualizacao = serializers.DateTimeField(format='%s')
    data_vigencia = serializers.DateField(format='%s')

    class Meta:
        model = TabelaPreco
        fields = '__all__'
