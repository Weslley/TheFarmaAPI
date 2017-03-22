from django.db import models
from api.utils import tipo_cartao
from django.core.validators import MinLengthValidator


class Cartao(models.Model):
    nome_proprietario = models.CharField(max_length=60)
    token = models.CharField(max_length=160, null=True, blank=True)
    numero_cartão = models.CharField(max_length=4)
    tipo = models.IntegerField(default=tipo_cartao.CREDITO, choices=tipo_cartao.CHOICES)
    cvv = models.CharField(max_length=4, validators=[MinLengthValidator(3), ])
    bandeira = models.CharField(max_length=20)
