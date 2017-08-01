from django.db import models

from api.models.adiantamento import Adiantamento
from api.models.enums import StatusContaReceber
from api.models.farmacia import Farmacia
from api.models.pedido import Pedido


class ContaReceberFarmacia(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='contas_receber_farmacia')
    status = models.IntegerField(choices=StatusContaReceber.choices(), default=StatusContaReceber.ABERTA)
    farmacia = models.ForeignKey(Farmacia, related_name='contas_receber')
    data_vencimento = models.DateField()
    data_credito = models.DateTimeField(null=True, blank=True)
    adiantamento = models.OneToOneField(Adiantamento, null=True, related_name='parcelas_adiantadas', blank=True)
    valor_adiantamento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_administradora_cartao = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_administradora_cartao = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    @property
    def valor_liquido(self):
        """
        Property para imprimir o valor liquido de acodo com o valor bruto e demais variaveis
        :return: Valor liquido da parcela
        """
        return self.valor_bruto - self.valor_administradora_cartao - self.valor_thefarma - self.valor_adiantamento

    @property
    def numero_parcela(self):
        """
        Número da parcela
        :return: Número da parcela
        """
        return 0

