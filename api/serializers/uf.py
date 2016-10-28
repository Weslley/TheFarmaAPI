from rest_framework import serializers

from api.models.uf import Uf
from api.serializers.tabela_preco import TabelaPrecoSerializer


class UfSerializer(serializers.ModelSerializer):
    tabela_preco = TabelaPrecoSerializer()

    class Meta:
        model = Uf
        fields = '__all__'
