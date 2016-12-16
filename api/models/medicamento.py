from django.db import models

from api.utils import tipo_medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.laboratorio import Laboratorio


class Medicamento(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    principio_ativo = models.ForeignKey(PrincipioAtivo)
    laboratorio = models.ForeignKey(Laboratorio)
    tipo = models.IntegerField(choices=tipo_medicamento.CHOICES)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)


class MedicamentoApExport(models.Model):
    familia = models.IntegerField(null=True, blank=True)
    principioAtivo_id = models.IntegerField()
    classe = models.IntegerField(null=True, blank=True)
    subClasse = models.IntegerField(null=True, blank=True)
    laboratorio_id = models.IntegerField()
    codbarras = models.CharField(null=True, blank=True, max_length=13)
    codbarras2 = models.CharField(null=True, blank=True, max_length=13)
    codbarras3 = models.CharField(null=True, blank=True, max_length=13)
    tipoPreco = models.CharField(null=True, blank=True, max_length=1)
    lista = models.CharField(null=True, blank=True, max_length=1)
    vazio = models.CharField(null=True, blank=True, max_length=1)
    generico = models.BooleanField()
    descricao = models.CharField(max_length=100)
    apresentacao = models.CharField(max_length=100)
    dataVigencia = models.DateField(null=True, blank=True)
    dataDesconhecida = models.DateField(null=True, blank=True)
    pmf19 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmf18 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmf17 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmf12 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmc19 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmc18 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmc17 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pmc12 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    registroMS = models.CharField(max_length=15, null=True, blank=True)
    portaria = models.CharField(max_length=10, null=True, blank=True)
