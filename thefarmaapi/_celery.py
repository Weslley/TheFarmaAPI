# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thefarmaapi.settings')

app = Celery('thefarmaapi')

app.config_from_object('thefarmaapi.settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
