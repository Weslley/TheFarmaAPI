from django.db import models
from api.models.endereco import Endereco


class Laboratorio(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    nome_completo = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.OneToOneField(Endereco)

    class Meta:
        ordering = ('nome', 'nome_completo')
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.nome_completo if self.nome_completo else self.id)
