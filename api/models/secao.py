from django.db import models


class Secao(models.Model):
    nome = models.CharField(max_length=80)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.nome
