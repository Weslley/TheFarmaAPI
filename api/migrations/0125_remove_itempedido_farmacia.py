# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-23 11:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0124_auto_20171023_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itempedido',
            name='farmacia',
        ),
    ]
