# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0114_auto_20171004_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamentocartao',
            name='captura_status',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pagamentocartao',
            name='pagamento_status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
