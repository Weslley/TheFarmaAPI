# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-04 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20161224_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituicao',
            name='site',
            field=models.URLField(default='http://'),
        ),
        migrations.AlterField(
            model_name='post',
            name='conteudo',
            field=models.TextField(blank=True, null=True, verbose_name='Conteúdo'),
        ),
        migrations.AlterField(
            model_name='post',
            name='url_referencia',
            field=models.URLField(blank=True, null=True, verbose_name='URL Referência'),
        ),
    ]