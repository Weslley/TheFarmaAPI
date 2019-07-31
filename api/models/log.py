from django.db import models


class Log(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
