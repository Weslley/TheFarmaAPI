from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import (CustomJSONAPIView, IsAuthenticatedMixin,
                             LogoutMixin)
from api.models.cliente import Cliente
from api.serializers.cliente import ClienteSerializer
from api.serializers.user import (CreateUserClienteSerializer,
                                  LoginDefautSerializer,
                                  LoginFacebookSerializer,
                                  LoginFarmaciaSerializer, LoginSerializer,
                                  UserSerializer)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(APIView, CustomJSONAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        data = self.get_data(request)

        # Autenticando o usuario
        usuario = authenticate(username=data['email_telefone'], password=data['password'])

        # Se o mesmo existir, gero o token
        if usuario:
            if hasattr(usuario, 'cliente') and usuario.cliente:
                cliente_serializer = ClienteSerializer(instance=usuario.cliente)
                return Response(cliente_serializer.data, status=status.HTTP_200_OK)

        return Response({'detail': 'Email/Telefone ou senha incorretos'}, status=status.HTTP_404_NOT_FOUND)


class LoginFacebook(APIView, CustomJSONAPIView):
    serializer_class = LoginFacebookSerializer

    def post(self, request, format=None):
        data = self.get_data(request)

        # Autenticando o usuario
        try:
            usuario = User.objects.get(cliente__facebook_id=data['facebook_id'])
        except User.DoesNotExist:
            usuario = None
        except:
            return Response({'detail': 'Erro inesperado'}, status=status.HTTP_404_NOT_FOUND)

        # Se o mesmo existir, gero o token
        if usuario:
            token, create = Token.objects.get_or_create(user=usuario)

            # caso esteja fazendo a requisição do login novamente, reseta o token
            if not create:
                token.delete()
                token = Token.objects.create(user=usuario)

            data = {
                'id': usuario.id,
                'foto': 'http://thefarmaapi.herokuapp.com' + usuario.cliente.foto.url if hasattr(usuario, 'cliente') and usuario.cliente.foto else '',
                'nome': usuario.first_name,
                'sobrenome': usuario.last_name,
                'email': usuario.email,
                'token': token.key
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Usuario não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class Logout(IsAuthenticatedMixin, LogoutMixin):
    """
    Requisição de logout. É necessário estar autenticado
    """

    pass


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserClienteSerializer


class LoginDefault(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginDefautSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TesteLogin(generics.CreateAPIView):
    serializer_class = LoginFacebookSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            usuario = User.objects.get(cliente__facebook_id=data['facebook_id'])
            serializer = self.get_serializer(usuario)
            data = dict(serializer.data)
            token, create = Token.objects.get_or_create(user=usuario)

            # caso esteja fazendo a requisição do login novamente, reseta o token
            if not create:
                token.delete()
                token = Token.objects.create(user=usuario)

            data['token'] = token.key
        except User.DoesNotExist:
            usuario = User.objects.create(
                first_name=data['nome'],
                last_name=data['sobrenome'] if 'sobrenome' in data else '',
                email=data['email'],
                username=data['facebook_id']
            )
            usuario.set_password(data['facebook_id'])
            usuario.save()
            cliente = Cliente()
            cliente.facebook_id = data['facebook_id']
            cliente.sexo = data['sexo'] if 'sexo' in data else ''
            cliente.usuario = usuario
            cliente.save()
            serializer = self.get_serializer(usuario)
            data = dict(serializer.data)
            token, create = Token.objects.get_or_create(user=usuario)

            # caso esteja fazendo a requisição do login novamente, reseta o token
            if not create:
                token.delete()
                token = Token.objects.create(user=usuario)

            data['token'] = token.key

        return Response(data, status=status.HTTP_201_CREATED)


class LoginFarmacia(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginFarmaciaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
