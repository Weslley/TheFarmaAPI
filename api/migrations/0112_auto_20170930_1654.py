# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-30 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0111_auto_20170923_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='bairro',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cep',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cidade',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='logradouro',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='nome_endereco',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='uf',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
