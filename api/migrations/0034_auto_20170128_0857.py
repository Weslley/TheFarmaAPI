# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-28 08:57
from __future__ import unicode_literals

from django.db import migrations, models

import misc.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20170127_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atualizacao',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='arquivos_atualizacao', validators=[misc.validators.validate_file_extension]),
        ),
    ]
