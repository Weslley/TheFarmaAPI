# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-08 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20170308_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
