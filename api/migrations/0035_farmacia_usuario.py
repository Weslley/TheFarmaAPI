# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-29 23:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0034_auto_20170128_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmacia',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
