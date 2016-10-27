from django.db import models
from api.models.uf import Uf


class Cidade(models.Model):
    ibge = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    uf = models.ForeignKey(Uf)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.uf)