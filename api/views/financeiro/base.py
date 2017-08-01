from rest_framework import generics
from rest_framework.response import Response
import calendar
import locale

from api.models.enums.status_conta_receber import StatusContaReceber
from api.models.pedido import Pedido
from api.models.conta_receber_farmacia import ContaReceberFarmacia
from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.serializers.pedido import PedidoSimplesSerializer
from api.serializers.conta_receber_farmacia import ContaReceberFarmaciaSerializer

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ResumoFinanceiro(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):

    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        # Filtrando as ultimas 4 vendas
        pedidos = Pedido.objects.filter(
            itens__farmacia__representantes=representante
        ).order_by('-id')[:4]

        # Filtrando as 4 ultimas contas recebidas
        contas_recebidas = ContaReceberFarmacia.objects.filter(
            status=StatusContaReceber.PAGA,
            farmacia__representantes=representante
        ).order_by('-data_credito')[:4]

        # Filtrando as próximas 4 contas a receber
        contas_a_receber = ContaReceberFarmacia.objects.filter(
            status=StatusContaReceber.ABERTA,
            farmacia__representantes=representante
        ).order_by('data_vencimento')[:4]

        # Valores calculados de rendimento de cada mês
        values = []
        for mes in range(1, 13):
            valor = 0.0
            valor += mes
            values.append(valor)

        data = {
            'pedidos': PedidoSimplesSerializer(pedidos, many=True).data,
            'contas_recebidas': ContaReceberFarmaciaSerializer(contas_recebidas, many=True).data,
            'contas_a_receber': ContaReceberFarmaciaSerializer(contas_a_receber, many=True).data,
            'rendimentos': {
                'labels': [n.upper() for n in calendar.month_name if n],
                'values': values
            }
        }
        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia
