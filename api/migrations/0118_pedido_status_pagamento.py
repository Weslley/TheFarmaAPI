# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 14:45
from __future__ import unicode_literals

import api.models.enums.status_pagamento
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0117_auto_20171007_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='status_pagamento',
            field=models.IntegerField(choices=[(0, 'ABERTO'), (1, 'PAGO'), (2, 'CANCELADO')], default=api.models.enums.status_pagamento.StatusPagamento(0)),
        ),
    ]
