from django.db import models


class Post(models.Model):
    titulo = models.CharField()
    imagem_perfil = models.ImageField()
    imagem = models.ImageField()
    video = models.URLField()
    conteudo = models.TextField()
    url_referencia = models.URLField()
    data_criacao = models.DateTimeField()
    data_atualizacao = models.DateTimeField()
    tipo = models.CharField()
    # usuario
