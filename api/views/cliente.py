from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.models.cliente import Cliente
from api.serializers.cliente import ClienteCreateSerializer
from api.serializers.user import DefaultUserSerializer


class ClienteCreate(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteCreateSerializer
    usuario = None

    def create(self, request, *args, **kwargs):
        data = request.data
        with transaction.atomic():
            user_serializer = DefaultUserSerializer(data=data)
            user_serializer.is_valid(raise_exception=True)
            usuario = user_serializer.save()

            raise Exception('Testando...')

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)