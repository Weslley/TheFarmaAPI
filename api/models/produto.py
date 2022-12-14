from api.models.enums import StatusProduto
from api.models.fabricante import Fabricante
from api.models.principio_ativo import PrincipioAtivo
from api.models.secao import Secao
from api.models.sintoma import Sintoma
from api.models.subsecao import Subsecao
from api.utils import tipo_produto
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    principio_ativo = models.ForeignKey(PrincipioAtivo)
    laboratorio = models.ForeignKey(Fabricante)
    tipo = models.IntegerField(choices=tipo_produto.CHOICES, default=tipo_produto.NAO_MEDICAMENTO)
    status = models.IntegerField(choices=StatusProduto.choices(), default=StatusProduto.REVISAR)
    secao = models.ForeignKey(Secao, null=True)
    subsecao = models.ForeignKey(Subsecao, null=True)
    sintomas = models.ManyToManyField(Sintoma, related_name='medicamentos_associados', blank=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now=True)
    descricao = models.TextField(null=True)

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)

    @property
    def tipo_venda(self):
        try:
            return self.principio_ativo.tipo_venda
        except Exception as error:
            return 0
    
    @property
    def get_manager(self):
        return self.__class__.objects

    def genericos(self):
        return self.get_manager.filter(principio_ativo=self.principio_ativo)


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
