# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-02 15:03
from __future__ import unicode_literals

import api.models.enums.status_pedido
import api.models.enums.status_produto
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_auto_20170801_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='status',
            field=models.IntegerField(choices=[(0, 'REVISAR'), (1, 'PUBLICADO'), (2, 'NEGADO')], default=api.models.enums.status_produto.StatusProduto(0)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.IntegerField(choices=[(0, 'ABERTO'), (1, 'ACEITO'), (2, 'AGUARDANDO_ENVIO_FARMACIA'), (3, 'AGUARDANDO_RETIRADA_CLIENTE'), (4, 'ENVIADO'), (5, 'ENTREGUE'), (6, 'CANCELADO_PELA_FARMACIA'), (7, 'CANCELADO_PELO_CLIENTE'), (8, 'SEM_PROPOSTA')], default=api.models.enums.status_pedido.StatusPedido(0)),
        ),
    ]