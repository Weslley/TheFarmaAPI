# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 16:09
from __future__ import unicode_literals

import api.models.enums.status_pagamento_cartao
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0115_auto_20171004_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamentocartao',
            name='status',
            field=models.IntegerField(choices=[(0, 'NOT_FINISHED'), (1, 'AUTHORIZED'), (2, 'PAYMENT_CONFIRMED'), (3, 'DENIED'), (10, 'VOIDED'), (11, 'REFUNDED'), (12, 'PENDING'), (13, 'ABORTED'), (20, 'SCHEDULED')], default=api.models.enums.status_pagamento_cartao.StatusPagamentoCartao(0)),
        ),
    ]
