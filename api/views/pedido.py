from django.db.models import Q
from django.http.response import Http404
from cieloApi3 import *
from django.http import JsonResponse
import json
from api.models.farmacia import Farmacia
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
    PropostaUpdateSerializer, PedidoDetalhadoSerializer, PedidoCheckoutSerializer, ComandaPeidoSerializer
from rest_framework import permissions, status as stts
from api.servico_pagamento.pagamento import Pagamento
from api.servico_pagamento import tipo_servicos
from api.models.enums.status_pagamento_cartao import StatusPagamentoCartao
from api.models.enums.status_pedido import StatusPedido
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.enums.tipo_venda import TipoVenda


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
        enviar_notif(pedido.cliente.fcm_token,TipoNotificacaoTemplate.VISUALIZADO,pedido.cliente.id,pedido,extra_data={'pedido_id':pedido.id})
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
        instance = self.get_queryset().filter(cliente=cliente).order_by('id').last()
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
        print("STATUS DO PEDIDO:>>>>>>"instance.status)
        instance = self.get_object()
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Proposta já foi cancelado.'})

        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Proposta já foi entregue.'})


        if instance.status == StatusPedido.ACEITO:
            delivery = instance.delivery

            # Verifica se existe medicamento de venda com receita, observando cada item...
            medicamento_receita = False
            for item in instance.itens.all():
                if(item.apresentacao.produto.principio_ativo.tipo_venda == TipoVenda.COM_RECEITA):
                    medicamento_receita = True
                    break
            # Verifica a forma de pagamento do pedido
            if(instance.forma_pagamento == FormaPagamento.DINHEIRO):
                if(medicamento_receita):
                    if(delivery):
                        tipo = TipoNotificacaoTemplate.D_AGUARDANDO_EM_DINHEIRO_COM_RECEITA
                    else:
                        tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_DINHEIRO_COM_RECEITA
                else:
                    if(delivery):
                        tipo = TipoNotificacaoTemplate.D_AGUARDANDO_EM_DINHEIRO_NORM
                    else:
                        tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_DINHEIRO_NORM

            elif(instance.forma_pagamento == FormaPagamento.EM_CARTAO):
                if(medicamento_receita):
                    if(delivery):
                        tipo = TipoNotificacaoTemplate.D_AGUARDANDO_EM_CARTAO_COM_RECEITA
                    else:
                        tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_CARTAO_COM_RECEITA
                else:
                    if(delivery):
                        tipo = TipoNotificacaoTemplate.D_AGUARDANDO_EM_CARTAO_NORM
                    else:
                        tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_CARTAO_NORM

            enviar_notif(instance.cliente.fcm_token,tipo,instance.cliente.id,extra_data={'pedido_id':instance})
            if(delivery):
                instance.status = StatusPedido.AGUARDANDO_ENVIO_FARMACIA
            else:
                instance.status = StatusPedido.AGUARDANDO_RETIRADA_CLIENTE
            instance.save()

        if instance.status == StatusPedido.ENVIADO:
            # Confirmando também a entrega
            instance.status = StatusPedido.ENTREGUE
            instance.save()
            #evento fcm
            quantidade = ItemPedido.objects.filter(pedido_id=instance.id)
            if (len(quantidade)==1):
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_S,instance.cliente.id,extra_data={'pedido_id':instance})
            else:
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_P,instance.cliente.id,extra_data={'pedido_id':instance})
        else:
            # confirmando envio
            instance.status = StatusPedido.ENVIADO
            instance.save()
            #gera mensagem no fcm
            #evento fcm
            quantidade = ItemPedido.objects.filter(pedido_id=instance.id)
            if (len(quantidade)==1):
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_SAIU_ENTREGA_S,instance.cliente.id,extra_data={'pedido_id':instance})
            else:
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.MEDICAMENTO_SAIU_ENTREGA_P,instance.cliente.id,extra_data={'pedido_id':instance}) 

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
        delivery = instance.delivery
        if instance.status == StatusPedido.CANCELADO_PELO_CLIENTE or\
                instance.status == StatusPedido.CANCELADO_PELA_FARMACIA:
            raise ValidationError({'detail': 'Proposta já foi cancelado.'})
        if instance.status == StatusPedido.ENTREGUE:
            raise ValidationError({'detail': 'Proposta já foi entregue.'})
            
        else:
            # confirmando envio
            quantidade = ItemPedido.objects.filter(pedido_id=instance.id)
            if (len(quantidade)==1):
                tipo = TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_S
            else:
                tipo = TipoNotificacaoTemplate.MEDICAMENTO_FORAM_ENTREGUE_P
            instance.status = StatusPedido.ENTREGUE
            enviar_notif(instance.cliente.fcm_token,tipo,instance.cliente.id,extra_data={'pedido_id':instance})
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UltimosPedidos(GenericAPIView):

    def get_queryset(self):
        return Pedido.objects.order_by('-data_atualizacao','-id').all()[:20]

    def get(self,request,*args, **kwargs):
        if self.request.user.is_anonymous():
            return Response({'error':'token não informado'},status=stts.HTTP_403_FORBIDDEN)
        #init vars
        qs = self.get_queryset()
        rs = []
        farmacias = []
        for item in qs:
            #recupera todas as farmacias que receberam
            try:
                for farmacia_id in item.farmacias_receberam.split(','):
                    try:
                        farmacias.append(Farmacia.objects.get(pk=farmacia_id).nome_fantasia)
                    except:
                        pass
            except:
                farmacias = []
            #prepara o retorno para cada pedido
            rs.append({
                'id':item.id,
                'data':item.data_atualizacao.strftime('%d %B %Y %H:%M'),
                'status':self.get_nome_status(item.status),
                'farmacias':farmacias
            })
            #zera
            farmacias = []

        return Response(rs)
    
    @staticmethod
    def get_nome_status(status):
        if status == 0:
            return 'ABERTO'
        elif status == 1 :
            return 'ACEITO'
        elif status == 2 :
            return 'AGUARDANDO_ENVIO_FARMACIA'
        elif status == 3 :
            return 'AGUARDANDO_RETIRADA_CLIENTE'
        elif status == 4 :
            return 'ENVIADO'
        elif status == 5 :
            return 'ENTREGUE'
        elif status == 6 :
            return 'CANCELADO_PELA_FARMACIA'
        elif status == 7 :
            return 'CANCELADO_PELO_CLIENTE'
        elif status == 8 :
            return 'SEM_PROPOSTA'
        elif status == 9 :
            return 'TIMEOUT'
    
class CancelaPagamento(GenericAPIView, IsRepresentanteAuthenticatedMixin):

    def get_queryset(self):
        return Pedido.objects.get(pk=self.kwargs.get('id',None))

    def get(self,request, *args, **kwargs):
        pedido = self.get_queryset()
        json_venda = pedido.json_venda
        try:
            data_cancelamento = {
                'payment_id':json_venda['Payment']['PaymentId']
            }
        except:
            return Response({'detail':'Venda sem captura de json'},status=stts.HTTP_400_BAD_REQUEST)
        if pedido.delivery:
            data_cancelamento.update({'valor':pedido.valor_bruto_sem_frete + pedido.valor_frete})
        else:
            data_cancelamento.update({'valor':pedido.get_total_farmacia(pedido.farmacia)})
        print(data_cancelamento)
        rs = Pagamento.cancelar(tipo_servicos.CIELO,data_cancelamento)
        if rs['cancelamento']['Status'] == StatusPagamentoCartao.PAGAMENTO_CANCELADO:
            #atualiza o pedido
            pedido.status = StatusPagamentoCartao.PAGAMENTO_CANCELADO
            pedido.save()
            return Response(status=stts.HTTP_200_OK)
        else:
            print(rs)
            return Response({'detail':'Cancelamento nao realizado, entre em contato com o suporte!'},status=stts.HTTP_400_BAD_REQUEST)

class ProblemasEntregaView(GenericAPIView, IsRepresentanteAuthenticatedMixin):

    def get_object(self):
        return Pedido.objects.get(id=self.kwargs.get('id'))

    def get(self,request,*args, **kwargs):
        #tipo equivale ao motivo de nao ter sido entregue
        tipo = request.GET.get('tipo',None)
        #recupera o pedido
        pedido = self.get_object()
        pedido.status = StatusPedido.NAO_ENTREGUE
        pedido.save()
        enviar_notif(pedido.cliente.fcm_token,tipo,pedido.cliente_id,pedido=pedido,extra_data={'pedido_id':pedido})
        return Response({})

class ComandaView(GenericAPIView,IsRepresentanteAuthenticatedMixin):

    def get_object(self):
        return Pedido.objects.get(pk=self.kwargs.get('id'))

    def get(self,request,*args,**kwargs):
        pedido = self.get_object()
        serializer = ComandaPeidoSerializer(pedido)
        return Response(serializer.data)
