# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-22 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0195_apresentacao_data_atualizacao_manual'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecoSugerido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True)),
                ('apresentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preco_sugerido_tabelas', to='api.Apresentacao')),
            ],
        ),
    ]
