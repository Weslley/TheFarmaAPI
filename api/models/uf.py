from django.db import models
from api.utils import ufs


class Uf(models.Model):
    sigla = models.CharField(max_length=2, choices=ufs.CHOICES)
    nome = models.CharField(max_length=20)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.sigla

    def __unicode__(self):
        return self.sigla
