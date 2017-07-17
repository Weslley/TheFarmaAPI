from django.db import models
from api.models.secao import Secao


class Subsecao(models.Model):
    nome = models.CharField(max_length=80)
    secao = models.ForeignKey(Secao, related_name='subsecoes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.nome
