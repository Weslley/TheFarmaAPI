from rest_framework import serializers
from api.models.tabela_preco import TabelaPreco
from api.serializers.uf import UfReduzidoSerializer


class TabelaPrecoSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()
    data_vigencia = serializers.SerializerMethodField()

    class Meta:
        model = TabelaPreco
        fields = '__all__'

    def get_data_vigencia(self, obj):
        from datetime import datetime
        a = datetime(obj.data_vigencia.year, obj.data_vigencia.month, obj.data_vigencia.day)
        return int(a.timestamp() * 1000)

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)
