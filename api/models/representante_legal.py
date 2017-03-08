from django.db import models
from api.models.farmacia import Farmacia
from django.contrib.auth.models import User
from api.models.endereco import Endereco


class RepresentanteLegal(models.Model):
    rg = models.CharField(verbose_name='RG', max_length=14, blank=True, null=True)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    telefone = models.CharField(max_length=11)
    cargo = models.CharField(max_length=60, null=True, blank=True)
    endereco = models.OneToOneField(Endereco)
    farmacia = models.ForeignKey(Farmacia, related_name='representantes')
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='representante_farmacia')

    class Meta:
        verbose_name = 'Representante legal'
        verbose_name_plural = 'Representantes legais'

    def __str__(self):
        return self.usuario.first_name
