from django.db import models

from api.models.cidade import Cidade


class Regiao(models.Model):
    cidade = models.ForeignKey(Cidade, related_name='regioes')
    nome = models.CharField(max_length=60)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.nome
