from django.db import models
from api.models.cidade import Cidade
from api.models.bairro import Bairro


class Endereco(models.Model):
    cep = models.CharField(max_length=8, null=True, blank=True)
    logradouro = models.CharField(max_length=80)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=10, null=True, blank=True)
    cidade = models.ForeignKey(Cidade)
    bairro = models.ForeignKey(Bairro)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
