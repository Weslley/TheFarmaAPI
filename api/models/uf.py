from django.db import models
from api.utils import ufs


class Uf(models.Model):
    sigla = models.CharField(max_length=2, choices=ufs.CHOICES)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome