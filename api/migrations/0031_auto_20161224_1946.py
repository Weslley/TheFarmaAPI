# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-24 19:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_medicamentoapexport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'NOTÍCIA'), (1, 'PATROCINADO'), (2, 'AVISO')], default=0),
        ),
        migrations.AlterField(
            model_name='usuarioinstituicao',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_instituicao', to=settings.AUTH_USER_MODEL),
        ),
    ]
