from django.db import models
from api.models.endereco import Endereco


class Laboratorio(models.Model):
    nome = models.CharField(max_length=110)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    endereco = models.OneToOneField(Endereco, null=True, blank=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.id)
