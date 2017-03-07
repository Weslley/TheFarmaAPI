# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-06 16:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0041_auto_20170306_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarioinstituicao',
            old_name='user',
            new_name='usuario',
        ),
        migrations.AlterUniqueTogether(
            name='usuarioinstituicao',
            unique_together=set([('instituicao', 'usuario')]),
        ),
    ]