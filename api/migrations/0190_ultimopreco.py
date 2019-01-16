# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-26 17:52
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0189_auto_20181220_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='UltimoPreco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=15, null=True)),
                ('apresentacao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ultimo_pedido_apresentacao', to='api.Apresentacao')),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ultimo_pedido_farmacia', to='api.Farmacia')),
            ],
        ),
    ]