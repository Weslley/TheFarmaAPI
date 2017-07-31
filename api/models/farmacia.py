from django.db import models

from api.models.conta_bancaria import ContaBancaria
from api.models.endereco import Endereco


class Farmacia(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    razao_social = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    logo = models.ImageField(upload_to='farmacias', null=True, blank=True)
    endereco = models.OneToOneField(Endereco)
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    conta_bancaria = models.OneToOneField(ContaBancaria)
    servico_entregador = models.BooleanField(default=True)
    servico_estoque = models.BooleanField(default=False)
    percentual_similar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_generico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_etico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_nao_medicamentos = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Farmácia'
        verbose_name_plural = 'Farmácias'

    def __str__(self):
        return self.razao_social
