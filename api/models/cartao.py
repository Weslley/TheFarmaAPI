from datetime import date

from django.core.validators import MinLengthValidator
from django.db import models

from api.models.cliente import Cliente
from api.utils import tipo_cartao


class Cartao(models.Model):
    nome_proprietario = models.CharField(max_length=60)
    token = models.CharField(max_length=160, null=True, blank=True)
    numero_cartao = models.CharField(max_length=4)
    tipo = models.IntegerField(default=tipo_cartao.CREDITO, choices=tipo_cartao.CHOICES)
    cvv = models.CharField(max_length=4, validators=[MinLengthValidator(3), ])
    bandeira = models.CharField(max_length=20)
    mes_expiracao = models.CharField(max_length=2, choices=[(str(value), str(value)) for value in list(range(1, 13))])
    ano_expiracao = models.CharField(max_length=4, choices=[(str(value), str(value)) for value in list(range(date.today().year, date.today().year + 101))])
    cliente = models.ForeignKey(Cliente, related_name='cartoes', on_delete=models.CASCADE)
    deletado = models.BooleanField(default=False)
