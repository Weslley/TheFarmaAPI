from django.db import models
from api.models.cidade import Cidade


class Bairro(models.Model):
    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome