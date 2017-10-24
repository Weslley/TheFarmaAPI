from django.db import models

from api.models.enums import StatusContaReceber
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.pedido import Pedido


class ContaReceber(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='contas_receber')
    status = models.IntegerField(choices=StatusContaReceber.choices(), default=StatusContaReceber.ABERTA)
    data_vencimento = models.DateField()
    valor_parcela = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_administradora_cartao = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_administradora_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    numero_parcela = models.IntegerField(default=1)
    valor_comissao = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    @property
    def valor_liquido_parcela(self):
        """
        Property para imprimir o valor liquido de acodo com o valor bruto e demais variaveis
        :return: Valor liquido da parcela
        """
        return self.valor_parcela - self.valor_administradora_cartao

    @property
    def valor_liquido_thefarma(self):
        """
        Valor
        :return:
        """
        return self.valor_comissao + (self.valor_administradora_thefarma - self.valor_administradora_cartao)

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

    @property
    def valor_administradora_cartao(self):
        return round((self.valor_parcela * self.percentual_administradora_cartao) / 100, 2)

    @property
    def valor_administradora_thefarma(self):
        return round((self.valor_parcela * self.percentual_administradora_thefarma) / 100, 2)
