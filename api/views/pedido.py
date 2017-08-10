from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.pedido import Pedido
from api.serializers.pedido import PedidoSimplesSerializer


class PedidoCreate(generics.ListCreateAPIView, IsAuthenticatedMixin):
    serializer_class = PedidoSimplesSerializer
    queryset = Pedido.objects.all()
