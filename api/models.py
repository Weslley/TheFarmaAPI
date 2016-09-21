# -*- coding: utf-8 -*-
from django.db import models
from api.utils import ufs, tipo_medicamento


class Medicamento(models.Model):
    nome = models.CharField(max_length=40, null=True, blank=True)
    principio_ativo = models.ForeignKey('PrincipioAtivo')
    laboratorio = models.ForeignKey('Laboratorio')
    tipo = models.IntegerField(choices=tipo_medicamento.CHOICES)

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)


class Apresentacao(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True)
    nome = models.CharField(max_length=60, null=True, blank=True)
    registro_ms = models.CharField(max_length=17, null=True, blank=True)
    imagem = models.ImageField(upload_to='apresentacoes')
    tabela = models.ForeignKey('TabelaPreco', related_name='apresentacoes')
    medicamento = models.ForeignKey(Medicamento, related_name='apresentacoes')

    def __str__(self):
        return self.nome if self.nome else self.medicamento


class TabelaPreco(models.Model):
    icm = models.DecimalField(max_digits=15, decimal_places=2)
    pmc = models.DecimalField(max_digits=15, decimal_places=2)
    pmf = models.DecimalField(max_digits=15, decimal_places=2)
    data_vigencia = models.DateField()

    class Meta:
        verbose_name = 'Tabela de preço'
        verbose_name_plural = 'Tabela de preços'


class Laboratorio(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    nome_completo = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.OneToOneField('Endereco')

    class Meta:
        ordering = ('nome', 'nome_completo')
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.nome_completo if self.nome_completo else self.id)


class PrincipioAtivo(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Princípio ativo'
        verbose_name_plural = 'Princípios ativo'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.id)


class Farmacia(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    razao_social = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    cliente_infog2 = models.BooleanField(verbose_name='Cliente INFOG2 ?', default=True)
    logo = models.ImageField(upload_to='farmacias')
    endereco = models.OneToOneField('Endereco')
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', blank=True, null=True)

    class Meta:
        verbose_name = 'Farmácia'
        verbose_name_plural = 'Farmácias'

    def __str__(self):
        return self.razao_social


class RepresentanteLegal(models.Model):
    nome = models.CharField(max_length=60)
    rg = models.CharField(verbose_name='RG', max_length=14, blank=True, null=True)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    telefone = models.CharField(max_length=11)
    endereco = models.OneToOneField('Endereco')
    farmacia = models.ForeignKey(Farmacia, related_name='representantes')

    class Meta:
        verbose_name = 'Representante legal'
        verbose_name_plural = 'Representantes legais'

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cep = models.CharField(max_length=8, null=True, blank=True)
    logradouro = models.CharField(max_length=80)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=10, null=True, blank=True)
    cidade = models.ForeignKey('Cidade')
    bairro = models.ForeignKey('Bairro')

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class Cidade(models.Model):
    ibge = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    uf = models.ForeignKey('Uf')

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.uf)


class Bairro(models.Model):
    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class Uf(models.Model):
    sigla = models.CharField(max_length=2, choices=ufs.CHOICES)
    nome = models.CharField(max_length=20)
    tabela_preco = models.ForeignKey(TabelaPreco, null=True, blank=True)

    def __str__(self):
        return self.nome
