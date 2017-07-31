from django.db import models

from api.models.banco import Banco
from api.models.farmacia import Farmacia


class ContaBancaria(models.Model):
    farmacia = models.ForeignKey(Farmacia, related_name='contas')
    banco = models.ForeignKey(Banco, related_name='contas_associadas')
    agencia = models.IntegerField()
    digito = models.CharField(max_length=1)
    numero_conta = models.IntegerField()
    digito_conta = models.CharField(max_length=1)
