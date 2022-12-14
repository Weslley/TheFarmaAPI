# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-16 12:06
from __future__ import unicode_literals

import api.models.enums.status_conta
import api.models.enums.status_pagamento_conta
import api.models.enums.status_pedido_faturamento
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0163_auto_20181004_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, 'ABERTA'), (1, 'PAGA'), (2, 'CANCELADA')], default=api.models.enums.status_pagamento_conta.StatusPagamentoConta(0))),
                ('tipo', models.IntegerField(choices=[(0, 'RECEBER'), (1, 'PAGAR')], default=api.models.enums.status_conta.StatusConta(1))),
                ('data_vencimento', models.DateField(blank=True, null=True)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas', to='api.Farmacia')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='status_faturamento',
            field=models.IntegerField(choices=[(0, 'NAO_FATURADO'), (1, 'FATURADO')], default=api.models.enums.status_pedido_faturamento.StatusPedidoFaturamento(0)),
        ),
    ]
