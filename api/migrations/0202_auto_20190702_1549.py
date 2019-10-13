# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-02 15:49
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0201_auto_20190702_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmacia',
            name='raio_acao',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='itempropostapedido',
            name='possui',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='itempropostapedido',
            name='quantidade',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]