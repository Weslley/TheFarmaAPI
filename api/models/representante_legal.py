from django.db import models
from api.models.farmacia import Farmacia
from api.models.endereco import Endereco


class RepresentanteLegal(models.Model):
    nome = models.CharField(max_length=60)
    rg = models.CharField(verbose_name='RG', max_length=14, blank=True, null=True)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    telefone = models.CharField(max_length=11)
    endereco = models.OneToOneField(Endereco)
    farmacia = models.ForeignKey(Farmacia, related_name='representantes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        verbose_name = 'Representante legal'
        verbose_name_plural = 'Representantes legais'

    def __str__(self):
        return self.nome
