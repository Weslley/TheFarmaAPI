# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 11:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_auto_20170905_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='numero_parcelas',
        ),
        migrations.AddField(
            model_name='pagamentocartao',
            name='numero_parcelas',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
