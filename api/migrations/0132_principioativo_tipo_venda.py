# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 17:28
from __future__ import unicode_literals

import api.models.enums.tipo_venda
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0131_contareceber_valor_comissao'),
    ]

    operations = [
        migrations.AddField(
            model_name='principioativo',
            name='tipo_venda',
            field=models.IntegerField(choices=[(0, 'SEM_RECEITA'), (1, 'COM_RECEITA'), (2, 'NAO_PERMITIDA')], default=api.models.enums.tipo_venda.TipoVenda(0)),
        ),
    ]
