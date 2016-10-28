from rest_framework import serializers
from api.models.tabela_preco import TabelaPreco


class TabelaPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPreco
        fields = '__all__'
