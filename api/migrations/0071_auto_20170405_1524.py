# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 15:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_cartao_cliente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartao',
            old_name='numero_cartão',
            new_name='numero_cartao',
        ),
    ]
