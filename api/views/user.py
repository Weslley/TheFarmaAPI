from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins.base import CustomJSONAPIView
from api.serializers.user import UserSerializer, LoginSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(APIView, CustomJSONAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        data = self.get_data(request)

        usuario = authenticate(username=data['email'], password=data['password'])
        if usuario:
            token = Token.objects.get_or_create(user=usuario)
            print(token)
            data = {
                'id': usuario.id,
                'foto': 'http://thefarmaapi.herokuapp.com' + usuario.perfil.foto.url if hasattr(usuario, 'perfil') and usuario.perfil.foto else '',
                'nome': usuario.first_name,
                'sobrenome': usuario.last_name,
                'email': usuario.email,
                'token': token[0].key
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Email ou senha incorretos'}, status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):
    pass
