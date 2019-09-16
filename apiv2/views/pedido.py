from api.models.pedido import Pedido
from api.permissions import IsOnlyCliente
from api.mixins.base import IsClienteAuthenticatedMixin
from api.consumers.farmacia import FarmaciaConsumer, PropostaSerializer

from apiv2.serializers.pedido import PedidoCreateSerializer, PedidoRetriveSerializer

from rest_framework import permissions
from rest_framework import generics, response


class PedidoCreateListView(generics.ListCreateAPIView, IsClienteAuthenticatedMixin):
    queryset = Pedido.objects.all()
    serializer_class = PedidoCreateSerializer
    permission_classes = (permissions.IsAuthenticated, IsOnlyCliente)


class PedidoRetriveView(generics.RetrieveAPIView, IsClienteAuthenticatedMixin):
    queryset = Pedido.objects.all()
    serializer_class = PedidoRetriveSerializer
    permission_classes = (permissions.IsAuthenticated,)