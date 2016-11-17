from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user import UserSerializer, LoginSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    model = User


class Logout(APIView):
    pass
