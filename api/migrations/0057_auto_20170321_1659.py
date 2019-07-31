# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-21 16:59
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_imagemapresentacao_capa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('imagem', models.ImageField(upload_to='unidades')),
            ],
        ),
        migrations.AddField(
            model_name='apresentacao',
            name='unidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Unidade'),
        ),
    ]
