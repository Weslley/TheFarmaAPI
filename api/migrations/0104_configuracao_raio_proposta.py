# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20170817_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracao',
            name='raio_proposta',
            field=models.FloatField(default=1.0),
        ),
    ]