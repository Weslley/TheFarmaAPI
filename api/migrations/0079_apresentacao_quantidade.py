# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_auto_20170726_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='apresentacao',
            name='quantidade',
            field=models.IntegerField(default=0),
        ),
    ]
