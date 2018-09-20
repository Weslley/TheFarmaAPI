import calendar
import locale
from datetime import date

from django.db.models import F, Q, Sum
from rest_framework import generics
from rest_framework.response import Response

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta_pagar import ContaPagar
from api.models.enums.status_conta_receber import StatusContaReceber
from api.models.enums.status_pedido import StatusPedido
from api.models.pedido import Pedido
from api.serializers.conta_receber_farmacia import \
    AnnotationContaReceberSerializer
from api.serializers.pedido import AnnotationPedidoSerializer

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ResumoFinanceiro(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):

    def ultimas_datas(self, status, limite=4):
        ultimos_models = ContaPagar.objects.filter(
            status=status, pedido__farmacia__representantes=self.get_object()
        ).distinct('data_vencimento')[:limite]

        return ultimos_models.values_list('data_vencimento')


    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        # Filtrando as ultimas 4 vendas
        pedidos = Pedido.objects.filter(
            farmacia__representantes=representante
        ).distinct('id').order_by('-id')[:4]

        ppedidos = Pedido.objects\
            .exclude(
                Q(status=StatusPedido.CANCELADO_PELA_FARMACIA) | 
                Q(status=StatusPedido.CANCELADO_PELO_CLIENTE)
            )\
            .filter(farmacia__representantes=representante)\
            .order_by('contas_receber__data_vencimento')\
            .annotate(data_criacao=F('contas_receber__data_vencimento'))\
            .values('data_criacao')\
            .annotate(
                valor_bruto=Sum('contas_receber__valor_parcela'),
                valor_liquido=Sum(
                    F('contas_receber__valor_parcela') -
                    F('contas_receber__valor_comissao')
                )
            )

        # Filtrando as 4 ultimas contas recebidas       
        datas_contas_recebidas = self.ultimas_datas(StatusContaReceber.PAGA, limite=50)
        contas_recebidas = ContaPagar.objects\
            .filter(
                data_vencimento__in=datas_contas_recebidas,
                status=StatusContaReceber.PAGA
            )\
            .order_by('-data_vencimento')\
            .values('data_vencimento')\
            .annotate(valor_liquido=Sum('valor_liquido'))

        # Filtrando as próximas 4 contas a receber
        datas_contas_a_receber = self.ultimas_datas(StatusContaReceber.ABERTA, limite=50)
        contas_a_receber = ContaPagar.objects\
            .filter(
                data_vencimento__in=datas_contas_a_receber,
                status=StatusContaReceber.ABERTA
            )\
            .order_by('data_vencimento')\
            .values('data_vencimento')\
            .annotate(valor_liquido=Sum('valor_liquido'))

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
                .aggregate(total=Sum('contas_receber__valor_parcela'))

            valor = float(query['total']) if query['total'] else 0
            values.append(valor)

        data = {
            'pedidos': AnnotationPedidoSerializer(ppedidos, many=True).data,
            'contas_recebidas': AnnotationContaReceberSerializer(contas_recebidas, many=True).data,
            'contas_a_receber': AnnotationContaReceberSerializer(contas_a_receber, many=True).data,
            'rendimentos': {
                'labels': [n.upper() for n in calendar.month_name if n],
                'values': values
            }
        }

        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia
