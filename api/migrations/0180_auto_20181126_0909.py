# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-26 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0179_auto_20181126_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apresentacao',
            name='comercializado',
            field=models.BooleanField(default=True),
        ),
    ]
