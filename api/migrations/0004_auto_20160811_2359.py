# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 23:59
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160811_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoMedicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('quantidade', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Grupo de medicamento',
                'verbose_name_plural': 'Grupos de medicamento',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('nome_completo', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Laboratório',
                'verbose_name_plural': 'Laboratórios',
                'ordering': ('nome', 'nome_completo'),
            },
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_barras', models.BigIntegerField(blank=True, null=True)),
                ('registro', models.CharField(blank=True, max_length=17, null=True)),
                ('nome', models.CharField(blank=True, max_length=40, null=True)),
                ('nome_complementar', models.CharField(blank=True, max_length=40, null=True)),
                ('generico', models.BooleanField(default=False)),
                ('tipo', models.IntegerField(default=0)),
                ('preco_maximo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.GrupoMedicamento')),
                ('laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Laboratorio')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PrincipioAtivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Princípio ativo',
                'verbose_name_plural': 'Princípios ativo',
                'ordering': ('nome',),
            },
        ),
        migrations.AddField(
            model_name='medicamento',
            name='principio_ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.PrincipioAtivo'),
        ),
        migrations.AddField(
            model_name='grupomedicamento',
            name='principio_ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.PrincipioAtivo'),
        ),
    ]
