# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-31 22:51
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20170131_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representantelegal',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='representante_farmacia', to=settings.AUTH_USER_MODEL),
        ),
    ]
