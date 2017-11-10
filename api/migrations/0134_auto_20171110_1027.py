# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20171110_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'GENÉRICO'), (1, 'SIMILAR'), (2, 'ÉTICO'), (3, 'NÃO MEDICAMENTO')], default=3),
        ),
    ]
