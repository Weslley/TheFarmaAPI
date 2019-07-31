# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-31 17:15
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_auto_20170731_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_domindo_final',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_domindo_inicial',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_feriado_final',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_feriado_inicial',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_sabado_final',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_sabado_inicial',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_segunda_sexta_final',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='horario_funcionamento_segunda_sexta_inicial',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='tempo_entrega',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
