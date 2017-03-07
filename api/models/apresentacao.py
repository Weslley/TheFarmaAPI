from django.db import models

from api.models.produto import Produto


class Apresentacao(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    registro_ms = models.CharField(max_length=17, null=True, blank=True)
    imagem = models.ImageField(upload_to='apresentacoes', null=True, blank=True)
    produto = models.ForeignKey(Produto, related_name='apresentacoes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome if self.nome else self.medicamento
