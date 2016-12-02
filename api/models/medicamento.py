from django.db import models

from api.utils import tipo_medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.laboratorio import Laboratorio


class Medicamento(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    principio_ativo = models.ForeignKey(PrincipioAtivo)
    laboratorio = models.ForeignKey(Laboratorio)
    tipo = models.IntegerField(choices=tipo_medicamento.CHOICES)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)
