from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from api.models.cliente import Cliente, ClienteEndereco
from api.models.endereco import Endereco
from api.permissions import IsOwnerClienteEndereco
from api.serializers.cliente import ClienteSerializer
from api.serializers.endereco import EnderecoSerializer
from api.serializers.user import CreateUserSerializer
from api import permissions
from rest_framework.permissions import IsAuthenticated


class ClienteCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticatedInGetPut, )

    def login(self, usuario, password):
        authenticate(username=usuario.email, password=password)

    def send_email_confirmation(self, usuario):
        print('Enviou email de confirmação')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            cliente = Cliente.objects.create(
                usuario=user,
                telefone=serializer.validated_data['telefone'] if 'telefone' in serializer.validated_data else None
            )
            cliente_serializer = ClienteSerializer(instance=cliente)
            headers = self.get_success_headers(serializer.data)
            self.login(user, serializer.validated_data['password'])
            self.send_email_confirmation(user)
            return Response(cliente_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ClienteSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClienteSerializer(instance=instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()

    def get_object(self):
        queryset = Cliente.objects.all()

        obj = get_object_or_404(queryset, **{'usuario': self.request.user})

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class EnderecoCreate(generics.ListCreateAPIView):
    serializer_class = EnderecoSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Endereco.objects.filter(
            clienteendereco___cliente__usuario=self.request.user
        )
        return queryset

    def perform_create(self, serializer):
        with transaction.atomic():
            cliente = self.request.user.cliente
            instance = serializer.save()

            if instance.principal:
                for item in cliente.enderecos.all():
                    endereco = item.endereco
                    endereco.principal = False
                    endereco.save()

            ClienteEndereco.objects.create(
                _cliente=cliente,
                endereco=instance
            )


class EnderecoUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = (IsAuthenticated, IsOwnerClienteEndereco)
    lookup_url_kwarg = 'id'

    def perform_update(self, serializer):
        with transaction.atomic():
            cliente = self.request.user.cliente
            instance = serializer.save()

            if instance.principal:
                for item in cliente.enderecos.all():
                    endereco = item.endereco
                    if endereco.id != instance.id:
                        endereco.principal = False
                        endereco.save()


class CartaoCreate():
    pass


class CartaoRetreive():
    pass


class CartaoUpdate():
    pass


class CartaoDelete():
    pass
