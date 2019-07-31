# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-05 23:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20180202_0514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regiao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('data_atualizacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de atualização')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regioes', to='api.Cidade')),
            ],
        ),
        migrations.AddField(
            model_name='bairro',
            name='regiao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bairros', to='api.Regiao'),
        ),
    ]
