from django.db import models


class Bairro(models.Model):
    cidade = models.ForeignKey('Cidade', related_name='bairros')
    regiao = models.ForeignKey('Regiao', related_name='bairros', blank=True, null=True)
    nome = models.CharField(max_length=60)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return self.nome
