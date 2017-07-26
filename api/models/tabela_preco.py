from django.db import models

from api.models.apresentacao import Apresentacao
from api.models.uf import Uf


class TabelaPreco(models.Model):
    icms = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmc = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmf = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_vigencia = models.DateField(null=True, blank=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    apresentacao = models.ForeignKey(Apresentacao, related_name='tabelas')

    class Meta:
        verbose_name = 'Tabela de preço'
        verbose_name_plural = 'Tabela de preços'
        unique_together = ('apresentacao', 'icms')
