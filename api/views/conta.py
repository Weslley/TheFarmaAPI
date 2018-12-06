from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce

from rest_framework import generics
from rest_framework.response import Response

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta import Conta
from api.models.pedido import Pedido
from api.models.enums import FormaPagamento, StatusPedidoFaturamento
from api.serializers.conta import ContaSerializer
from api.serializers.farmacia import FarmaciaSimplificadoSerializer
from api.pagination import SmallResultsSetPagination


class ContaList(generics.ListAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Lista as contas de faturamento relacionadas ao 
    representante que fez a requisicao
    """
    serializer_class = ContaSerializer
    pagination_class = SmallResultsSetPagination

    def get_representante(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia

    def get_queryset(self):
        representante = self.get_representante()
        return Conta.objects.filter(
            farmacia__representantes=representante
        ).order_by('-data_vencimento')


class ContaRetrieve(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Detalhe das conta de faturamento
    """
    def get_object(self):
        self.check_object_permissions(
            self.request, self.request.user.representante_farmacia
        )
        return self.request.user.representante_farmacia

    def get(self, request, *args, **kwargs):
        representante = self.get_object()
        farmacia = representante.farmacia
        requested_pk = self.kwargs.get('pk')

        conta = Conta.objects.filter(
            farmacia__representantes=representante,
            pk=requested_pk
        ).first()

        pedidos_faturados = Pedido.objects.filter(
            faturamento=conta,
            status_faturamento=StatusPedidoFaturamento.FATURADO
        )

        detalhes_credito = pedidos_faturados.all().aggregate(
            taxa_adm=Coalesce(Sum('valor_comissao_administradora'), V(0)),
            comissoes=Coalesce(Sum('valor_comissao_thefarma'), V(0)),
        )

        detalhes_credito.update(
            pedidos_faturados.filter(
                forma_pagamento=FormaPagamento.CARTAO
            ).aggregate(
                credito=Coalesce(Sum('valor_bruto'), V(0))
            )
        )

        detalhes_faturamento = pedidos_faturados.filter(
            forma_pagamento=FormaPagamento.DINHEIRO
        ).aggregate(
            dinheiro=Coalesce(Sum('valor_liquido'), V(0))
        )

        detalhes_faturamento.update(
            pedidos_faturados.filter(
                forma_pagamento=FormaPagamento.CARTAO
            ).aggregate(
                cartao_de_credito=Coalesce(Sum('valor_liquido'), V(0))
            )
        )

        data = {
            'farmacia': FarmaciaSimplificadoSerializer(farmacia, many=False).data,
            'conta': ContaSerializer(conta, many=False).data,
            'detalhes_credito': detalhes_credito,
            'detalhes_faturamento': detalhes_faturamento
        }

        return Response(data)
