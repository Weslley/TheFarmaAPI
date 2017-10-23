from django.db import models

from api.models.enums import StatusContaReceber
from api.models.pedido import Pedido


class ContaReceberThefarma(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='contas_receber_thefarma')
    status = models.IntegerField(choices=StatusContaReceber.choices(), default=StatusContaReceber.ABERTA)
    data_vencimento = models.DateField()
    valor_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_administradora_cartao = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_administradora_cartao = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_credito = models.DateField(null=True)
    numero_parcela = models.IntegerField(default=1)

    @property
    def valor_liquido(self):
        """
        Property para imprimir o valor liquido de acodo com o valor bruto e demais variaveis
        :return: Valor liquido da parcela
        """
        return self.valor_bruto - self.valor_administradora_cartao
