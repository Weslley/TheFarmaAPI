# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-23 22:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_feriado'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feriado',
            unique_together=set([('dia', 'mes', 'uf')]),
        ),
    ]
