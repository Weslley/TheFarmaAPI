# -*- coding: utf-8 -*-
from django.db import models

from api.utils import UFs


class Farmacia(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    razao_social = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    cliente_infog2 = models.BooleanField(verbose_name='Cliente INFOG2 ?', default=True)
    cep = models.CharField(verbose_name='CEP', max_length=8, blank=True, null=True)
    logradouro = models.CharField(max_length=150)
    numero = models.IntegerField(verbose_name='Número')
    cidade = models.ForeignKey('Cidade', related_name='farmacias')
    bairro = models.CharField(max_length=150)
    complemento = models.CharField(max_length=150, blank=True, null=True)
    nome_responsavel = models.CharField(verbose_name='Nome', max_length=60)
    sobrenome_responsavel = models.CharField(verbose_name='Sobrenome', max_length=60, blank=True, null=True)
    rg_responsavel = models.CharField(verbose_name='RG', max_length=14, blank=True, null=True)
    cpf_responsavel = models.CharField(verbose_name='CPF', max_length=11)
    telefone_responsavel = models.CharField(verbose_name='Telefone', max_length=11)
    cep_responsavel = models.CharField(verbose_name='CEP', max_length=8, blank=True, null=True)
    logradouro_responsavel = models.CharField(verbose_name='Logradouro', max_length=150, blank=True, null=True)
    numero_responsavel = models.IntegerField(verbose_name='Número', blank=True, null=True)
    cidade_responsavel = models.ForeignKey('Cidade', verbose_name='Cidade',  related_name='responsaveis_farmacias', blank=True, null=True)
    bairro_responsavel = models.CharField(verbose_name='Bairro', max_length=150, blank=True, null=True)
    complemento_responsavel = models.CharField(verbose_name='Complemento', max_length=150, blank=True, null=True)
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', blank=True, null=True)

    class Meta:
        verbose_name = 'Farmácia'
        verbose_name_plural = 'Farmácias'
        ordering = ('-id', )

    def __str__(self):
        return self.razao_social


class Cidade(models.Model):
    ibge = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    uf = models.CharField(max_length=2, choices=UFs)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.uf)


class Medicamento(models.Model):
    codigo_barras = models.BigIntegerField(null=True, blank=True)
    registro = models.CharField(max_length=17, null=True, blank=True)
    nome = models.CharField(max_length=40, null=True, blank=True)
    nome_complementar = models.CharField(max_length=60, null=True, blank=True)
    grupo = models.ForeignKey('GrupoMedicamento', null=True, blank=True)
    principio_ativo = models.ForeignKey('PrincipioAtivo')
    laboratorio = models.ForeignKey('Laboratorio')
    generico = models.BooleanField(default=False)
    tipo = models.IntegerField(default=0)
    preco_maximo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)


class PrincipioAtivo(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Princípio ativo'
        verbose_name_plural = 'Princípios ativo'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.id)


class Laboratorio(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    nome_completo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('nome', 'nome_completo')
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.nome_completo if self.nome_completo else self.id)


class GrupoMedicamento(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    principio_ativo = models.ForeignKey(PrincipioAtivo)
    quantidade = models.IntegerField(default=0)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Grupo de medicamento'
        verbose_name_plural = 'Grupos de medicamento'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.principio_ativo)