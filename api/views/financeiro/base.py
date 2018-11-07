import calendar
import locale
from datetime import date

from django.db.models import Q, Sum
from rest_framework import generics
from rest_framework.response import Response

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta import Conta
from api.models.pedido import Pedido
from api.models.enums.status_pedido import StatusPedido
from api.serializers.conta import ContaSerializer
from api.serializers.pedido import PedidoTotaisSerializer, PedidoMinimalSerializer

from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ResumoListagemVendas(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Resumo da listagem de vendas
    * Implementacoes de filtros
    """
    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        hoje = datetime.now()
        pedidos_de_hoje = Pedido.objects\
            .exclude(
                Q(status=StatusPedido.CANCELADO_PELA_FARMACIA) | 
                Q(status=StatusPedido.CANCELADO_PELO_CLIENTE)
            )\
            .filter(
                farmacia__representantes=representante,
                data_criacao__year=hoje.year,
                data_criacao__month=hoje.month,
                data_criacao__day=hoje.day
            )

        valores_pedidos =  pedidos_de_hoje.aggregate(
            bruto=Sum('valor_bruto'),
            liquido=Sum('valor_liquido')
        )

        for k, v in valores_pedidos.items():
            if v == None:
                valores_pedidos[k] = 0

        data = {
            'resumo': {
                'valor_bruto': valores_pedidos.get('bruto'),
                'valor_liquido': valores_pedidos.get('liquido'),
                'quantidade': pedidos_de_hoje.count()
            },
            'data': PedidoMinimalSerializer(pedidos_de_hoje, many=True).data,
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
            .exclude(
                Q(status=StatusPedido.CANCELADO_PELA_FARMACIA) | 
                Q(status=StatusPedido.CANCELADO_PELO_CLIENTE)
            )\
            .filter(
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
                .exclude(
                    Q(status=StatusPedido.CANCELADO_PELA_FARMACIA) | 
                    Q(status=StatusPedido.CANCELADO_PELO_CLIENTE)
                )\
                .filter(
                    log__data_criacao__month=mes,
                    log__data_criacao__year=date.today().year,
                    farmacia__representantes=representante,
                )\
                .aggregate(total=Sum('valor_bruto'))

            valor = float(query['total']) if query['total'] else 0
            values.append(valor)

        data = {
            'conta_atual': ContaSerializer(contas.first(), many=False).data,
            'contas': ContaSerializer(contas[:6], many=True).data,
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
