from datetime import timedelta

from django.db import models


class Configuracao(models.Model):
    duracao_proposta = models.DurationField(default=timedelta(minutes=5))
    raio_proposta = models.FloatField(default=1.0)
