# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-31 22:48
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0035_farmacia_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmacia',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='representantelegal',
            name='nome',
        ),
        migrations.AddField(
            model_name='representantelegal',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
