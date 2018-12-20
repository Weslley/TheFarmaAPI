# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-19 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0185_auto_20181130_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificacoesTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tela', models.IntegerField(null=True)),
                ('titulo', models.CharField(max_length=50)),
                ('mensagem', models.TextField(blank=True, null=True)),
                ('tipo', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='apresentacao',
            name='data_atualizacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de atualização'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='data_atualizacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de atualização'),
        ),
    ]