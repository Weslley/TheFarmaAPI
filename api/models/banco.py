from django.db import models


class Banco(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome
