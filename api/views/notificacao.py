from rest_framework import generics
from api.pagination import DefaultResultsSetPagination
from api.mixins.base import IsClienteAuthenticatedMixin
from api.models.notificacao import Notificacao
from api.serializers.notificacao import NotificacaoSerializer, NotificacaoUpdateSerializer



class NotificacaoList(generics.ListAPIView, IsClienteAuthenticatedMixin):
    """
    **GET** Lista todas as notificações do usuário autenticado
    """
    serializer_class = NotificacaoSerializer
    pagination_class = DefaultResultsSetPagination

    def get_queryset(self):
        """
        Filtrando pelo cliente da requisição
        :return: Queryset
        """
        queryset = Notificacao.objects.filter(cliente=self.request.user.cliente).order_by('-data_criacao')
        return queryset



class NotificacaoUpdate(generics.RetrieveUpdateAPIView, IsClienteAuthenticatedMixin):
    """
    **GET** Lista todas as notificações do usuário autenticado
    """
    serializer_class = NotificacaoUpdateSerializer

    def get_queryset(self):
        """
        Filtrando pelo cliente da requisição
        :return: Queryset
        """
        queryset = Notificacao.objects.filter(cliente=self.request.user.cliente).order_by('-data_criacao')
        return queryset
