# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 14:55
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_auto_20170330_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartao',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cartoes', to='api.Cliente'),
            preserve_default=False,
        ),
    ]
