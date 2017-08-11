from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.pedido import Pedido
from api.serializers.pedido import PedidoSerializer


class PedidoCreate(generics.ListCreateAPIView, IsAuthenticatedMixin):
    """
    Cria(POST)/Lista(GET) pedido(os)

    **POST** Cria um pedido para o usuário autenticado que enviará propostas
    para as farmacias que atendam os requisitos do mesmo

    **GET** Lista todos os pedidos do usuário autenticado

    """
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()
