import locale
from rest_framework import serializers

from api.models.pedido import Pedido

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class PedidoSimplesSerializer(serializers.ModelSerializer):
    data_criacao = serializers.DateTimeField(read_only=True, source='log.data_criacao')
    valor_bruto = serializers.SerializerMethodField()
    valor_liquido = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ('id', 'data_criacao', 'valor_bruto', 'valor_liquido', 'status')

    def get_valor_bruto(self, obj):
        return locale.currency(obj.valor_bruto, grouping=True, symbol=None)

    def get_valor_liquido(self, obj):
        return locale.currency(obj.valor_liquido, grouping=True, symbol=None)