from django.db import models
from api.models.uf import Uf
from django.core.validators import MinValueValidator, MaxValueValidator


class Feriado(models.Model):
    descricao = models.CharField(max_length=120)
    dia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    mes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    uf = models.ForeignKey(Uf, null=True, blank=True)

    def __str__(self):
        return self.descricao
