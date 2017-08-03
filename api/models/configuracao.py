from django.db import models
from datetime import timedelta


class Configuracao(models.Model):
    percentual_credito_avista_farmacia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_parcelado_farmacia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_avista_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_parcelado_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    duracao_proposta = models.DurationField(default=timedelta(minutes=5))
