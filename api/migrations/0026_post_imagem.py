# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-02 11:36
from __future__ import unicode_literals

from django.db import migrations, models

import api.models.post


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_remove_post_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.post.generate_filename),
        ),
    ]
