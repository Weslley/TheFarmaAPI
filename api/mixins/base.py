from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.atualizacao import Atualizacao
from datetime import datetime


class IsAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class IsFullAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória por sessão e token
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)


class CustomJSONAPIView(object):
    """
    Mixin para APIView de dados básicos
    """
    serializer_class = None

    def get_data(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            return serializer.create(serializer.validated_data)
        except:
            return None


class LogoutMixin(CustomJSONAPIView):

    serializer_class = None

    def post(self, request, format=None):
        try:
            token = request._auth
            token.delete()
        except Token.DoesNotExist:
            return Response({'detail': 'Token inválido.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)


class SyncApiMixin(GenericAPIView):
    lookup_url_kwarg = 'data'

    def get_queryset(self):
        long_data = self.kwargs['data']
        ultima_atualizacao = datetime.fromtimestamp(float(long_data) / 1000.0)
        if ultima_atualizacao:
            return self.queryset.filter(data_atualizacao__gte=ultima_atualizacao)
        else:
            return self.queryset.none()
