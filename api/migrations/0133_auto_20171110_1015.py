# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_principioativo_tipo_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apresentacao',
            name='codigo_barras',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]