# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-07 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20170306_1655'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Medicamento',
            new_name='Produto',
        ),
    ]
