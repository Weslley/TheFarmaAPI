# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-14 15:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_auto_20171014_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='quantidade_atendida',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
