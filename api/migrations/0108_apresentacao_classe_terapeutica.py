# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0107_auto_20170919_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='apresentacao',
            name='classe_terapeutica',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]