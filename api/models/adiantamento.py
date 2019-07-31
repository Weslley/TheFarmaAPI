from django.db import models

from api.models.log import Log


class Adiantamento(models.Model):
    log = models.OneToOneField(Log)
    percentual_adiantamento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
