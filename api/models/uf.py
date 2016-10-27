from django.db import models
from api.models.tabela_preco import TabelaPreco
from api.utils import ufs


class Uf(models.Model):
    sigla = models.CharField(max_length=2, choices=ufs.CHOICES)
    nome = models.CharField(max_length=20)
    tabela_preco = models.ForeignKey(TabelaPreco, null=True, blank=True)

    def __str__(self):
        return self.nome