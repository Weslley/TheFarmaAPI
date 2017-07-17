from django.db import models


class Unidade(models.Model):
    nome = models.CharField(max_length=40)
    imagem = models.ImageField(upload_to='unidades')
