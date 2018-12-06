# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-19 10:41
from __future__ import unicode_literals

import api.models.boleto
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0172_pedido_faturamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to=api.models.boleto.generate_filename)),
                ('codigo_de_barras', models.CharField(blank=True, max_length=275, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='data_emissao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='boleto',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedido', to='api.Boleto'),
        ),
    ]