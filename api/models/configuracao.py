from datetime import timedelta
from django.db import models
from api.models.administradora import Administradora


class Configuracao(models.Model):
    duracao_proposta = models.DurationField(default=timedelta(minutes=5))
    raio_proposta = models.FloatField(default=1.0)
    peso_ranking_visualizacao = models.FloatField(default=1.0)
    peso_ranking_proposta = models.FloatField(default=1.25)
    peso_ranking_compra = models.FloatField(default=1.5)
    administradora = models.OneToOneField(Administradora, null=True, blank=True)
    zenvia_conta = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name='Conta Zenvia')
    zenvia_password = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name='Codigo Zenvia')
