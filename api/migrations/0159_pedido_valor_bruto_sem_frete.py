# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-03 10:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0158_farmacia_valor_frete'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='valor_bruto_sem_frete',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
