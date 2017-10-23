from django.db import models

from api.models.enums import StatusContaReceber
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.pedido import Pedido


class ContaReceberThefarma(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='contas_receber_thefarma')
    status = models.IntegerField(choices=StatusContaReceber.choices(), default=StatusContaReceber.ABERTA)
    data_vencimento = models.DateField()
    valor_parcela = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_credito = models.DateField(null=True)
    numero_parcela = models.IntegerField(default=1)

    @property
    def valor_liquido(self):
        """
        Property para imprimir o valor liquido de acodo com o valor bruto e demais variaveis
        :return: Valor liquido da parcela
        """
        return self.valor_parcela

    @property
    def devedor(self):
        """
        Retorna o devedor da parcela
        :return:
        """
        if self.pedido.forma_pagamento == FormaPagamento.CARTAO:
            return self.pedido.administradora_cartao
        else:
            return self.pedido.farmacia
