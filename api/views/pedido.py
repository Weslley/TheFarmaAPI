from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.pedido import Pedido
from api.serializers.pedido import PedidoSerializer


class PedidoCreate(generics.ListCreateAPIView, IsAuthenticatedMixin):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()
