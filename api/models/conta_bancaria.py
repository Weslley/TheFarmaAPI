from django.db import models

from api.models.banco import Banco


class ContaBancaria(models.Model):
    banco = models.ForeignKey(Banco, related_name='contas_associadas')
    numero_agencia = models.IntegerField()
    digito_agencia = models.CharField(max_length=1)
    numero_conta = models.IntegerField()
    digito_conta = models.CharField(max_length=1)
    operacao = models.CharField(max_length=3, null=True, blank=True)
