from django.db import models

from api.models.uf import Uf


class Cidade(models.Model):
    ibge = models.IntegerField(primary_key=True, verbose_name='Código IBGE')
    nome = models.CharField(max_length=150)
    uf = models.ForeignKey(Uf, verbose_name='UF')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.uf)
