from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.pedido import Pedido
from api.pagination import SmallResultsSetPagination
from api.permissions import IsOnlyCliente
from api.serializers.pedido import PedidoCreateSerializer, PedidoSerializer


class PedidoCreate(generics.ListCreateAPIView, IsAuthenticatedMixin):
    """
    Cria(POST)/Lista(GET) pedido(os)

    **POST** Cria um pedido para o usuário autenticado que enviará propostas
    para as farmacias que atendam os requisitos do mesmo

    **GET** Lista todos os pedidos do usuário autenticado

    """
    pagination_class = SmallResultsSetPagination
    permission_classes = (IsOnlyCliente, )

    def get_queryset(self):
        """
        Filtrando pelo cliente da requisição
        :return: Queryset
        """
        queryset = Pedido.objects.filter(cliente=self.request.user.cliente)
        return queryset

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return PedidoSerializer
        return PedidoCreateSerializer
