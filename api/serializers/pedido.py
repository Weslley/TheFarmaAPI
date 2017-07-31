from rest_framework import serializers

from api.models.pedido import Pedido


class PedidoSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'data_credito', 'valor_bruto', 'valor_bruto', 'valor_liquido')

