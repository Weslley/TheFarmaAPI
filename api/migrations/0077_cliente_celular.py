# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_auto_20170726_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='celular',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
    ]

    # def apply(self, project_state, schema_editor, collect_sql=False):
    #     return project_state.clone()

    # def unapply(self, project_state, schema_editor, collect_sql=False):
    #     return project_state.clone()
