# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-05 23:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0146_migrate_manual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='bairro',
        ),
    ]
