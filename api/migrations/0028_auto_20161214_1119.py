# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 11:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0027_auto_20161206_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social', models.CharField(max_length=120)),
                ('nome_fantasia', models.CharField(max_length=70)),
                ('cpf_cnpj', models.CharField(max_length=14, verbose_name='CPF/CNPJ')),
                ('site', models.URLField()),
                ('logo', models.ImageField(upload_to='instituicoes')),
                ('telefone', models.CharField(max_length=11)),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de atualização')),
            ],
            options={
                'verbose_name': 'Instituição',
            },
        ),
        migrations.CreateModel(
            name='UsuarioInstituicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='api.Instituicao')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instituicao', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usuarioinstituicao',
            unique_together=set([('instituicao', 'user')]),
        ),
    ]
