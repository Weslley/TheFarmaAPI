from django.contrib.sites.models import Site
from rest_framework import generics

from api.pagination import SmallResultsSetPagination
from api.mixins.base import IsClienteAuthenticatedMixin
from api.models.pedido import Pedido
from api.serializers.pedido import PedidoSerializer, PedidoCreateSerializer, PropostaSerializer


class PedidoCreate(generics.ListCreateAPIView, IsClienteAuthenticatedMixin):
    """
    Cria(POST)/Lista(GET) pedido(os)

    **POST** Cria um pedido para o usuário autenticado que enviará propostas
    para as farmacias que atendam os requisitos do mesmo

    **GET** Lista todos os pedidos do usuário autenticado

    """
    serializer_class = PedidoCreateSerializer
    pagination_class = SmallResultsSetPagination

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
        Site.objects.get_current(request=self.request)
        if self.request.method.lower() == 'get':
            return PedidoSerializer
        return PedidoCreateSerializer

class PropostasList(generics.ListAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PropostaSerializer
