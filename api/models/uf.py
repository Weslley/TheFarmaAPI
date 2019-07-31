from datetime import datetime

from django.db import models

from api.utils import ufs


class Uf(models.Model):
    sigla = models.CharField(max_length=2, choices=ufs.CHOICES, unique=True)
    nome = models.CharField(max_length=20)
    icms = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.sigla

    def __unicode__(self):
        return self.sigla

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.data_atualizacao = datetime.now()
        return super(Uf, self).save(force_insert, force_update, using, update_fields)
