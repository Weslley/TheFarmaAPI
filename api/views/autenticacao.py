from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from api.mixins.base import (
    LogoutMixin,
    IsAuthenticatedMixin
)
from api.serializers.cliente import ClienteSerializer
from api.serializers.user import (
    EnviarCodigoSmsSerializer,
    LoginClienteSerializer,
    LoginDefautSerializer,
    LoginFarmaciaSerializer,
    CreateUserClienteSerializer
)


class Logout(IsAuthenticatedMixin, LogoutMixin):
    """
    Requisição de logout. É necessário estar autenticado
    """
    pass


class CreateUser(generics.CreateAPIView):
    """
    Metodo para criar cliente, mesmo metodo para cadastrar manualmente, e pelo facebook_id, o mesmo em é um dos campos
    opcionais
    """
    queryset = User.objects.all()
    serializer_class = CreateUserClienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        serializer = ClienteSerializer(instance=instance.cliente, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginCliente(generics.GenericAPIView):
    """
    URL de login do cliente, para login comum é obrigatório do email e senha, caso queira fazer o login
    com facebook, basta ignorar os campos de email e password, deixando em branco ou pode preenche-los se quiser
    """
    queryset = User.objects.all()
    serializer_class = LoginClienteSerializer


class EnviarCodigoSmsView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EnviarCodigoSmsSerializer


class LoginFarmacia(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginFarmaciaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
