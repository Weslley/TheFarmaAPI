# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0130_auto_20171024_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='contareceber',
            name='valor_comissao',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
