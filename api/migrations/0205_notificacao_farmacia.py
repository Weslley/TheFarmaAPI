# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-19 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0204_itempropostapedido_permutacao_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacao',
            name='farmacia',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Farmacia'),
        ),
    ]
