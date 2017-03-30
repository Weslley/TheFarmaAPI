# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-30 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_cliente_email_confirmado'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteEndereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='api.Cliente')),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Endereco')),
            ],
        ),
    ]
