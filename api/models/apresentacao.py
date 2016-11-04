from django.db import models

from api.models.medicamento import Medicamento


class Apresentacao(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    registro_ms = models.CharField(max_length=17, null=True, blank=True)
    imagem = models.ImageField(upload_to='apresentacoes', null=True, blank=True)
    medicamento = models.ForeignKey(Medicamento, related_name='apresentacoes')

    def __str__(self):
        return self.nome if self.nome else self.medicamento