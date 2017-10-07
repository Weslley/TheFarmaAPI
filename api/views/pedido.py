from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView, \
    GenericAPIView
from rest_framework.response import Response

from api.mixins.edit import UpdateAPIViewNoPatch
from api.models.enums.status_pedido import StatusPedido
from api.pagination import SmallResultsSetPagination
from api.mixins.base import IsClienteAuthenticatedMixin, IsRepresentanteAuthenticatedMixin, FarmaciaSerializerContext
from api.models.pedido import Pedido
from api.serializers.pedido import PedidoSerializer, PedidoCreateSerializer, PropostaSerializer, \
    PropostaUpdateSerializer, PedidoDetalhadoSerializer, PedidoCheckoutSerializer


class PedidoCreate(ListCreateAPIView, IsClienteAuthenticatedMixin):
    """
    Cria(POST)/Lista(GET) pedido(os)

    **POST** Cria um pedido para o usuário autenticado que enviará propostas
    para as farmacias que atendam os requisitos do mesmo

    **GET** Lista todos os pedidos do usuário autenticado

    """
    serializer_class = PedidoCreateSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """
        Filtrando pelo cliente da requisição
        :return: Queryset
        """
        queryset = Pedido.objects.filter(cliente=self.request.user.cliente)
        return queryset

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return PedidoSerializer
        return PedidoCreateSerializer


class PedidoRetrieve(RetrieveAPIView, IsClienteAuthenticatedMixin):
    lookup_url_kwarg = 'id'
    serializer_class = PedidoDetalhadoSerializer
    queryset = Pedido.objects.all()


class UltimoPedido(RetrieveAPIView, IsClienteAuthenticatedMixin):
    lookup_url_kwarg = 'id'
    serializer_class = PedidoDetalhadoSerializer
    queryset = Pedido.objects.all()

    def get_object(self):
        cliente = self.request.user.cliente
        instance = self.get_queryset().filter(cliente=cliente).last()
        if not instance:
            raise Http404('Nenhum pedido encontrado.')

        return instance


class PropostaList(ListAPIView, IsRepresentanteAuthenticatedMixin, FarmaciaSerializerContext):
    """
    Lista(GET) propostas

    **GET** Lista todos as propostas do usuário autenticado

    """
    serializer_class = PropostaSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """
        Filtrando pela farmacia da requisição
        :return: Queryset
        """
        queryset = Pedido.objects.filter(
            itens_proposta__farmacia=self.request.user.representante_farmacia.farmacia
        ).order_by('status', '-log__data_criacao').distinct()
        return queryset


class PropostaRetrieveUpdate(RetrieveUpdateAPIView, IsRepresentanteAuthenticatedMixin, FarmaciaSerializerContext):
    """
    Metodo para fazer o update ou o get das insformações de uma proposta
    """
    lookup_url_kwarg = 'id'
    serializer_class = PropostaUpdateSerializer
    queryset = Pedido.objects.all()

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return PropostaSerializer
        return PropostaUpdateSerializer


class PedidoCheckout(UpdateAPIViewNoPatch, IsClienteAuthenticatedMixin):
    """
    Metodo para o cliente fazer o checkout do pedido informando
    a farmacia selecionada, e os pagamentos
    """
    lookup_url_kwarg = 'id'
    serializer_class = PedidoCheckoutSerializer
    queryset = Pedido.objects.all()


class PedidoCancelamentoCliente(GenericAPIView, IsClienteAuthenticatedMixin):
    """
    Cancelamento de pedido por parte do cliente

    **POST** Cancelamento de pedido
    """
    lookup_url_kwarg = 'id'
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or \
            instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Pedido já foi cancelado.'})

        if instance.status == StatusPedido.TIMEOUT:
            raise ValidationError({'detail': 'Tempo excedido para realizar qualquer operação.'})

        if instance.status == StatusPedido.SEM_PROPOSTA:
            raise ValidationError({'detail': 'Não houve propostas para este pedido.'})

        if instance.status == StatusPedido.ENVIADO:
            raise ValidationError({'detail': 'Pedido já foi enviado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Pedido já foi entregue.'})

        # Cancelando o pedido
        instance.status = StatusPedido.CANCELADO_PELO_CLIENTE
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PedidoCancelamentoFarmacia(object):
    pass
