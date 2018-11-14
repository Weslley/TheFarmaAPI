# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-13 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0171_logdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='faturamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos', to='api.Conta'),
        ),
    ]
