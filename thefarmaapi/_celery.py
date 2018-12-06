# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thefarmaapi.settings')

app = Celery('thefarmaapi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, call_period_tasks.s())

@app.task(queue='periodicos')
def call_period_tasks():
    from api.tasks.contas import faturamento, alterar_status_contas
    faturamento()
    alterar_status_contas()
