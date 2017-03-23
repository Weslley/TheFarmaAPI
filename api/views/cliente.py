from rest_framework import generics
from api.models.cliente import Cliente
from api.serializers.cliente import ClienteCreateSerializer


class ClienteCreate(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteCreateSerializer
