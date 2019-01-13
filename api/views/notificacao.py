from rest_framework import generics, permissions, status as stts
from api.pagination import DefaultResultsSetPagination
from api.mixins.base import IsClienteAuthenticatedMixin
from api.models.notificacao import Notificacao
from rest_framework.response import Response
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


class VisualizarNotificacao(generics.GenericAPIView):
    """
    Muda a notificacao como visualizada
    """
    

    def get_queryset(self):
        return Notificacao.objects.get(pk=self.kwargs.get('id'))

    def get(self,request, *args, **kwargs):
        if self.request.user.is_anonymous():
            return Response({'error':'token não informado'},status=stts.HTTP_403_FORBIDDEN)
        notificao = self.get_queryset()
        notificao.visualizada = True
        notificao.save()
        return Response({
            'visualizada':notificao.visualizada
        })