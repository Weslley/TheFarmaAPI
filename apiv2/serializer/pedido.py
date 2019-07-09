from rest_framework import serializers
from api.models.pedido import Pedido

class PedidoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = (
            'id',
        )