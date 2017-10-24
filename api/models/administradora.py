from django.db import models

from api.models.log import Log
from datetime import datetime


class Administradora(models.Model):
    nome = models.CharField(max_length=60)
    log = models.OneToOneField(Log)
    dias_recebimento = models.IntegerField(default=1)
    percentual_credito_avista_farmacia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_parcelado_farmacia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_avista_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_credito_parcelado_thefarma = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.log:
            self.log.data_atualizacao = datetime.now()
            self.log.save(using=using)
        else:
            self.log = Log.objects.create()
        return super(Administradora, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )