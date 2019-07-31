from django.db import models

from api.models.adiantamento import Adiantamento
from api.models.enums import StatusContaReceber
from api.models.farmacia import Farmacia
from api.models.pedido import Pedido


class ContaPagar(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='contas_pagar')
    status = models.IntegerField(choices=StatusContaReceber.choices(), default=StatusContaReceber.ABERTA)
    data_vencimento = models.DateField()
    data_criacao = models.DateField(auto_now_add=True)
    valor_liquido = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    numero_parcela = models.IntegerField(default=1)
