from rest_framework import serializers

from api.models.pedido import Pedido


class PedidoSimplesSerializer(serializers.ModelSerializer):
    data_criacao = serializers.DateTimeField(read_only=True, source='log.data_criacao')

    class Meta:
        model = Pedido
        fields = ('id', 'data_criacao', 'valor_bruto', 'valor_liquido', 'status')

