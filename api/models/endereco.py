from django.db import models
from api.models.cidade import Cidade
from api.models.bairro import Bairro


class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=80)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, related_name='enderecos')
    bairro = models.ForeignKey(Bairro)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    nome_endereco = models.CharField(max_length=40)
    nome_destinatario = models.CharField(max_length=80, null=True, blank=True)
    principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
