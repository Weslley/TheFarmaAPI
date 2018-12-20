# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-20 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0187_auto_20181219_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apresentacao',
            name='dosagem',
            field=models.DecimalField(decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='apresentacao',
            name='segunda_dosagem',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='apresentacao',
            name='terceira_dosagem',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
    ]