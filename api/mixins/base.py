from datetime import datetime

from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.atualizacao import Atualizacao
from api.permissions import IsOnlyCliente, IsOnlyRepresentante


class IsAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    _authentication_classes = (authentication.TokenAuthentication,)
    _permission_classes = (permissions.IsAuthenticated,)

    def __init__(self, **kwargs):
        super(IsAuthenticatedMixin, self).__init__(**kwargs)
        self.authentication_classes = [_ for _ in self.authentication_classes]
        for _ in self._authentication_classes:
            self.authentication_classes.append(_)
        self.authentication_classes = tuple(self.authentication_classes)

        self.permission_classes = [_ for _ in self.permission_classes]
        for _ in self._permission_classes:
            self.permission_classes.append(_)
        self.permission_classes = tuple(self.permission_classes)


class IsFullAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória por sessão e token
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)


class IsRepresentantePermission(permissions.BasePermission):
    """
    Permissão para representante
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'representante_farmacia') and request.user.representante_farmacia

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return hasattr(request.user, 'representante_farmacia') and request.user.representante_farmacia


class IsAuthenticatedRepresentanteMixin(APIView):
    """
    Mixin para representante logado
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsRepresentantePermission)


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


class IsClienteAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOnlyCliente)


class IsRepresentanteAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOnlyRepresentante)
