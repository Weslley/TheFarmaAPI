# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-07 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20170307_1129'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Instituicao',
            new_name='Parceiro',
        ),
        migrations.RenameModel(
            old_name='UsuarioInstituicao',
            new_name='UsuarioParceiro',
        ),
        migrations.AlterModelOptions(
            name='parceiro',
            options={'verbose_name': 'Parceiro'},
        ),
    ]