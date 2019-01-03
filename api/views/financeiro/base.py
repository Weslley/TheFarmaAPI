from django.db.models import Q, Sum
from rest_framework import generics,permissions, status
from rest_framework.response import Response

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta import Conta
from api.models.pedido import Pedido, LogData, ItemPropostaPedido, ItemPedido
from api.models.enums.status_pedido import StatusPedido
from api.serializers.conta import ContaMinimalSerializer
from api.serializers.pedido import PedidoTotaisSerializer, \
    PedidoMinimalSerializer, LogDataSerializer, VendaPedido
from api.serializers.medicamento import MedicamentoRelatorio
from django.db.models import F, Q
from datetime import datetime, date
import calendar
import locale
import decimal


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ResumoListagemVendas(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Resumo da listagem de vendas
    """
    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        params = request.query_params
        flag = True
        filtro = {}

        if params.get('mes'):
            data_ref = datetime.strptime(params.get('mes'), '%B')
            filtro.update(
                {'data_criacao__month': data_ref.month}
            )
            flag = False

        if params.get('ano'):
            filtro.update(
                {'data_criacao__year': params.get('ano')}
            )
            flag = False

        if flag:
            hoje = datetime.now()
            filtro = {
                'data_criacao__year': hoje.year,
                'data_criacao__month': hoje.month,
                'data_criacao__day': hoje.day
            }

        pedidos_do_periodo = Pedido.objects\
            .filter(
                status=StatusPedido.ENTREGUE,
                farmacia__representantes=representante,
                **filtro
            )

        valores_pedidos = pedidos_do_periodo.aggregate(
            bruto=Sum('valor_bruto'),
            liquido=Sum('valor_liquido')
        )

        logs = LogData.objects.filter(farmacia__representantes=representante)

        for k, v in valores_pedidos.items():
            if v == None:
                valores_pedidos[k] = 0

        data = {
            'periodos': LogDataSerializer(logs, many=True).data,
            'resumo': {
                'valor_bruto': valores_pedidos.get('bruto'),
                'valor_liquido': valores_pedidos.get('liquido'),
                'quantidade': pedidos_do_periodo.count()
            },
            'data': PedidoMinimalSerializer(pedidos_do_periodo, many=True).data,
        }
        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class ResumoFinanceiro(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):

    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        # Filtrando as ultimas 4 vendas
        contas = Conta.objects.filter(
            farmacia__representantes=representante
        ).order_by('-data_vencimento')

        hoje = datetime.now()
        pedidos_de_hoje = Pedido.objects\
            .filter(
                status=StatusPedido.ENTREGUE,
                farmacia__representantes=representante,
                data_criacao__year=hoje.year,
                data_criacao__month=hoje.month,
                data_criacao__day=hoje.day
            )\
            .aggregate(
                bruto=Sum('valor_bruto'),
                liquido=Sum('valor_liquido')
            )

        # Valores calculados de rendimento de cada mês
        values = []
        for mes in range(1, 13):
            query = Pedido.objects\
                .filter(
                    status=StatusPedido.ENTREGUE,
                    log__data_criacao__month=mes,
                    log__data_criacao__year=date.today().year,
                    farmacia__representantes=representante,
                )\
                .aggregate(total=Sum('valor_bruto'))

            valor = float(query['total']) if query['total'] else 0
            values.append(valor)

        data = {
            'conta_atual': ContaMinimalSerializer(contas.first(), many=False).data,
            'contas': ContaMinimalSerializer(contas[:6], many=True).data,
            'vendas_hoje': PedidoTotaisSerializer(pedidos_de_hoje, many=False).data,
            'rendimentos': {
                'labels': [n.upper() for n in calendar.month_name if n],
                'values': values
            }
        }

        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class MedicamentosMaisVendidos(generics.GenericAPIView):
    """
    Recupera as vendas dos medicamentos
    recebe via parametro url(mes,ano)
    """

    def get(self,request,*args, **kwargs):
        #int vars
        mes = self.request.GET.get('mes',None)
        ano = self.request.GET.get('ano',None)
        if not (mes and ano):
            return Response({'error':'Parametros mes e ano são necessario'},status=status.HTTP_400_BAD_REQUEST)
        representante = self.get_object()
        medicamentos = []

        #pega todos os pedidos entregues
        pedidos = Pedido.objects.filter(
            status=StatusPedido.ENTREGUE,
            farmacia__representantes=representante,
            data_criacao__year=ano,
            data_criacao__month=mes,
        )

        valores = pedidos.aggregate(bruto=Sum('valor_bruto'),liquido=Sum('valor_liquido'))
        #calcula o total bruto e liquido
        #intera nos itens dos pedidos que a farmacia vendeu
        for pedido in pedidos:
            itens_pedido = ItemPedido.objects.filter(
                pedido=pedido,
            )
            #add in rs
            for item in itens_pedido:
                medicamentos.append(MedicamentoRelatorio(item).data)

        #recupera os medicamentos

        return Response({
            'total_numero_vendas':len(pedidos),
            'total_liquido':'{}'.format(locale.currency(valores['liquido'])),
            'total_bruto':'R$ {}'.format(locale.currency(valores['bruto'])),
            'medicamentos':medicamentos
        })
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia

class MedicamentosMaisVendidosDetalhes(generics.GenericAPIView):
    """
    recupera detalhes das vendas de um produto
    recebe via parametro url(mes,ano)
    """

    def get(self,request,*args, **kwargs):
        representante = self.get_object()
        mes = request.GET.get('mes',None)
        ano = request.GET.get('ano',None)
        rs_vendas = []
        valor_liquido = decimal.Decimal(0)
        valor_bruto = decimal.Decimal(0)
        id = self.kwargs.get('id')
        if not (mes and ano):
            return Response({'error':'Parametros mes e ano são necessario'},status=status.HTTP_400_BAD_REQUEST)
        
        #recupera todas os pedidos que contem o medicamento
        itens_pedido = ItemPedido.objects.filter( 
            Q(pedido__farmacia__representantes=representante) \
            & Q(pedido__data_criacao__year=ano)\
            & Q(pedido__data_criacao__month=mes)\
            & Q(apresentacao__produto__id=id)
        )

        for item in itens_pedido:
            valor_liquido += item.total_liquido
            valor_bruto += item.total_bruto

        #monta todas as vendas
        for item in itens_pedido:
            rs_vendas.append(VendaPedido(item).data)
        
        return Response({
            'total_vendas':len(itens_pedido),
            'total_liquido':locale.currency(valor_liquido),
            'total_bruto':locale.currency(valor_bruto),
            'vendas':rs_vendas,
        })
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia