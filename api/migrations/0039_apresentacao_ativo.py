# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-06 09:00
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20170201_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='apresentacao',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
