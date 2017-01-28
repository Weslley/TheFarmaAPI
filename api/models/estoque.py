from django.db import models
from api.models.apresentacao import Apresentacao
from api.models.farmacia import Farmacia


class Estoque(models.Model):
    farmacia = models.ForeignKey(Farmacia)
    apresentacao = models.ForeignKey(Apresentacao)
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.apresentacao.nome)
