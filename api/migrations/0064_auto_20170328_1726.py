# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-28 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_secao_imagem'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='cliente',
        #     name='cpf',
        #     field=models.CharField(max_length=11, unique=True),
        # ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
