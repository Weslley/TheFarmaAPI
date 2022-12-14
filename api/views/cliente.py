from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.mixins.base import IsRepresentanteAuthenticatedMixin, IsClienteAuthenticatedMixin
from api.mixins.edit import (ClienteQuerysetOnly,
                             RetrieveUpdateDestroyAPIViewNoPatch)
from api.models.cartao import Cartao

from api.models.cliente import ClienteEndereco, Cliente
from api.models.endereco import Endereco
from api.pagination import SmallResultsSetPagination
from api.permissions import (IsOnlyCliente,
                             IsOwnerClienteCartao, IsOwnerClienteEndereco)
from api.serializers.cartao import CartaoSerializer
from api.serializers.cliente import ClienteNoTokenSerializer, ClienteSerializer
from api.serializers.endereco import EnderecoSerializer, EnderecoClienteCreateSerializer


class ClienteList(ListAPIView, IsRepresentanteAuthenticatedMixin):
    """
    Listagem de clientes

    **GET** Listagem de clientes para farmacias e para superusers
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteNoTokenSerializer
    pagination_class = SmallResultsSetPagination


class ClienteRetrieve(RetrieveUpdateAPIView, IsClienteAuthenticatedMixin):
    """
    Dados do cliente

    **GET** retorna dados do cliente passando seu ID, o mesmo estando autenticado, ou um superuser
    """
    lookup_url_kwarg = 'id'
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class EnderecoCreate(ListCreateAPIView, IsClienteAuthenticatedMixin):
    """
    Listagem e criação de endereços do cliente

    **GET** Listagem dos endereços do cliente autenticado

    **POST** Criação de endereço para o cliente autenticado
    """
    serializer_class = EnderecoClienteCreateSerializer

    def get_queryset(self):
        queryset = Endereco.objects.filter(
            clienteendereco___cliente__usuario=self.request.user
        )
        return queryset

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return EnderecoSerializer
        return EnderecoClienteCreateSerializer

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


class EnderecoUpdateDelete(RetrieveUpdateDestroyAPIView, IsClienteAuthenticatedMixin):
    """
    Recupera, atualiza e remove dados do endereço do cliente

    **GET** Retorna dados do endereço

    **PUT** Atualiza dados do endereço (obrigátório enviar todos os campos)

    **PATCH** Atualiza parcialmente dados do endereço

    **DELETE** Remove endereço
    """
    queryset = Endereco.objects.all()
    serializer_class = EnderecoClienteCreateSerializer
    lookup_url_kwarg = 'id'

    def get_permissions(self):
        perms = super(EnderecoUpdateDelete, self).get_permissions()
        perms.append(IsOwnerClienteEndereco())
        return perms

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return EnderecoSerializer
        return EnderecoClienteCreateSerializer

    def perform_update(self, serializer):
        with transaction.atomic():
            cliente = self.request.user.cliente
            instance = serializer.save()
            if instance.principal:
                #desativa o principal antigo
                for endereco in cliente.enderecos.all():
                    endereco.endereco.principal = False
                    endereco.save()
                #reativa o passado como principal
                instance.principal = True
                instance.save()


class CartaoCreate(ListCreateAPIView, IsClienteAuthenticatedMixin):
    """
    Listagem e criação de cartões do cliente

    **GET** Listagem dos cartões do cliente autenticado

    **POST** Criação de cartão para o cliente autenticado
    """
    serializer_class = CartaoSerializer

    def get_queryset(self):
        return Cartao.objects.filter(cliente=self.request.user.cliente, deletado=False)


class CartaoUpdateDelete(RetrieveUpdateDestroyAPIViewNoPatch, IsClienteAuthenticatedMixin):
    """
    Recupera, atualiza e remove dados do cartão do cliente

    **GET** Retorna dados do cartão

    **PUT** Atualiza dados do cartão (obrigátório enviar todos os campos)

    **DELETE** Remove cartão
    """
    serializer_class = CartaoSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return Cartao.objects.filter(cliente=self.request.user.cliente)

    def perform_destroy(self, instance):
        instance.deletado = True
        instance.save()

class FcmUpdate(GenericAPIView):
    """
    Atualiza o fcm do cliente
    """
    def post(self,request,*args,**kwargs):
        cliente = Cliente.objects.get(usuario_id=request.user.id)
        cliente.fcm_token = request.data.get('fcm',None)
        cliente.save()
        return Response({'fcm':cliente.fcm_token})