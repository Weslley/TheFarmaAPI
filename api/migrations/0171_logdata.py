# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-08 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0170_auto_20181104_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=75)),
                ('ano', models.IntegerField()),
                ('farmacia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs_pedidos', to='api.Farmacia')),
            ],
        ),
    ]