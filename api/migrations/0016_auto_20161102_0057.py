# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-02 00:57
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20161102_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apresentacao',
            name='codigo_barras',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
