from django.db import models
from django.contrib.postgres.fields import JSONField
from .enums.tipo_notificacao import TipoNotificacao


class Notificacao(models.Model):
    tipo = models.IntegerField(choices=TipoNotificacao.choices())
    titulo = models.CharField(max_length=50)
    mensagem = models.TextField(null=True, blank=True)
    visualizada = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=True, blank=True)
    cliente = models.ForeignKey(
        'Cliente',
        related_name='notificacoes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.titulo
