from django.db import models

from api.utils import tipo_medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.laboratorio import Laboratorio


class Medicamento(models.Model):
    nome = models.CharField(max_length=40, null=True, blank=True)
    principio_ativo = models.ForeignKey(PrincipioAtivo)
    laboratorio = models.ForeignKey(Laboratorio)
    tipo = models.IntegerField(choices=tipo_medicamento.CHOICES)

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)
