from django.db.models import Q
from django.http.response import Http404
from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.filters import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView, \
    GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.filters import OrderingFilter, PropostaFilter
from api.mixins.edit import UpdateAPIViewNoPatch
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.enums.status_pagamento import StatusPagamento
from api.models.enums.status_pedido import StatusPedido
from api.pagination import SmallResultsSetPagination, MinResultsSetPagination
from api.mixins.base import IsClienteAuthenticatedMixin, IsRepresentanteAuthenticatedMixin, FarmaciaSerializerContext
from api.models.pedido import Pedido, ItemPropostaPedido, ItemPedido
from api.models.notificacao import TipoNotificacaoTemplate
from api.utils.firebase_utils import enviar_notif
from api.consumers import FarmaciaConsumer
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
        queryset = Pedido.objects.filter(cliente=self.request.user.cliente).order_by('-log__data_criacao')
        return queryset

    def get_serializer_class(self):
        """
        Selecionando o serializer de acordo do o tipo de metodo HTTP
        :return: SerializerClass
        """
        if self.request.method.lower() == 'get':
            return PedidoSerializer
        return PedidoCreateSerializer


class PropostaAddView(APIView):
    def get_object(self, id):
        try:
            return Pedido.objects.get(id=id)
        except Pedido.DoesNotExist:
            raise Http404('Nenhum pedido encontrado.')

    def post(self, request, id, format=None):
        pedido = self.get_object(id)
        actual_views = int(0 if pedido.views is None else pedido.views)
        pedido.views = actual_views + 1
        pedido.save()
        #notificacao fcm
        enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.VISUALIZADO,pedido.cliente.id)

        return Response({})


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
    pagination_class = MinResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PropostaFilter
    ordering_fields = ('log__data_criacao', '-log__data_criacao')
    ordering = ('-log__data_criacao',)

    def get_queryset(self):
        """
        Filtrando pela farmacia da requisição
        :return: Queryset
        """
        queryset = Pedido.objects.filter(
            itens_proposta__farmacia=self.request.user.representante_farmacia.farmacia,
        ).exclude(
            Q(status=StatusPedido.ABERTO) | Q(status=StatusPedido.AGUARDANDO_ENVIO_FARMACIA) | Q(status=StatusPedido.AGUARDANDO_RETIRADA_CLIENTE),
            itens_proposta__status=StatusItemProposta.ENVIADO,
            status_pagamento=StatusPagamento.ABERTO
        ).order_by('-log__data_criacao').distinct()
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
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Pedido já foi cancelado.'})

        if instance.status == StatusPedido.ENVIADO:
            raise ValidationError({'detail': 'Pedido já foi enviado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Pedido já foi entregue.'})

        # Cancelando o pedido
        instance.status = StatusPedido.CANCELADO_PELO_CLIENTE
        instance.save()
        serializer = self.get_serializer(instance)
        FarmaciaConsumer.notifica_cancelamento(instance, instance.farmacias)
        return Response(serializer.data)


class PropostaCancelamentoFarmacia(GenericAPIView, IsRepresentanteAuthenticatedMixin):
    """
    Cancelamento de proposta da farmacia

    **POST** Cancelamento de proposta
    """
    lookup_url_kwarg = 'id'
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Proposta já foi cancelado.'})

        if instance.status == StatusPedido.AGUARDANDO_ENVIO_FARMACIA or instance.status == StatusPedido.AGUARDANDO_RETIRADA_CLIENTE:
            raise ValidationError({'detail': 'Proposta ja foi aceito.'})

        if instance.status == StatusPedido.TIMEOUT:
            raise ValidationError({'detail': 'Tempo excedido para realizar qualquer operação.'})

        if instance.status == StatusPedido.ENVIADO:
            raise ValidationError({'detail': 'Proposta já foi enviado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Proposta já foi entregue.'})

        # Cancelando o proposta
        farmacia = request.user.representante_farmacia.farmacia
        instance.itens_proposta.filter(farmacia=farmacia).update(status=StatusItemProposta.CANCELADO)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConfirmarEnvio(GenericAPIView, IsRepresentanteAuthenticatedMixin):
    """
    Confirmar envio do pedido

    **POST** Confirmar envio do pedido
    """
    lookup_url_kwarg = 'id'
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Proposta já foi cancelado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Proposta já foi entregue.'})

        if instance.status == StatusPedido.ENVIADO:
            # Confirmando também a entrega
            instance.status = StatusPedido.ENTREGUE
            instance.save()
            #evento fcm
            quantidade = ItemPedido.objects.filter(pedido_id=instance.id)
            if (len(quantidade)==1):
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_S,instance.cliente.id)
            else:
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_P,instance.cliente.id)
        else:
            # confirmando envio
            instance.status = StatusPedido.ENVIADO
            instance.save()
            #gera mensagem no fcm
            #evento fcm
            quantidade = ItemPedido.objects.filter(pedido_id=instance.id)
            if (len(quantidade)==1):
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_SAIU_ENTREGA_S,instance.cliente.id)
            else:
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_SAIU_ENTREGA_P,instance.cliente.id) 

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConfirmarRetiradaEntrega(GenericAPIView, IsRepresentanteAuthenticatedMixin):
    """
    Confirmar entrega/retirada do pedido

    **POST** Confirmar entrega/retirada do pedido
    """
    lookup_url_kwarg = 'id'
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Proposta já foi cancelado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Proposta já foi entregue.'})

        # confirmando envio
        instance.status = StatusPedido.ENTREGUE
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
