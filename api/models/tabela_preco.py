from django.db import models

from api.models.apresentacao import Apresentacao
from api.models.uf import Uf


class TabelaPreco(models.Model):
    icms = models.DecimalField(max_digits=15, decimal_places=2)
    pmc = models.DecimalField(max_digits=15, decimal_places=2)
    pmf = models.DecimalField(max_digits=15, decimal_places=2)
    data_vigencia = models.DateField(null=True, blank=True)
    apresentacao = models.ForeignKey(Apresentacao, related_name='tabelas')
    ufs = models.ManyToManyField(Uf, blank=True)

    class Meta:
        verbose_name = 'Tabela de preço'
        verbose_name_plural = 'Tabela de preços'
