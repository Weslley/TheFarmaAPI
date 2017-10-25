# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-23 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0125_remove_itempedido_farmacia'),
    ]

    operations = [
        migrations.AddField(
            model_name='contapagar',
            name='numero_parcela',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='contareceberthefarma',
            name='numero_parcela',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='contapagar',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas_pagar', to='api.Pedido'),
        ),
    ]