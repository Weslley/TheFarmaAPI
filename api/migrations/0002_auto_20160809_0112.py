# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-09 01:12
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmacia',
            name='bairro_responsavel',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Bairro'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cep',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='CEP'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cep_responsavel',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='CEP'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cidade_responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsaveis_farmacias', to='api.Cidade', verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cliente_infog2',
            field=models.BooleanField(default=True, verbose_name='Cliente INFOG2 ?'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cnpj',
            field=models.CharField(max_length=14, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='complemento_responsavel',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='cpf_responsavel',
            field=models.CharField(max_length=11, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='data_atualizacao',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de atualização'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de criação'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='logradouro_responsavel',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Logradouro'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='nome_responsavel',
            field=models.CharField(max_length=60, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='numero',
            field=models.IntegerField(verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='numero_responsavel',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='rg_responsavel',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='RG'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='sobrenome_responsavel',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Sobrenome'),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='telefone_responsavel',
            field=models.CharField(max_length=11, verbose_name='Telefone'),
        ),
    ]
