# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-31 15:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_auto_20170731_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contabancaria',
            old_name='agencia',
            new_name='numero_agencia',
        ),
    ]