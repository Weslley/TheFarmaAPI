from django.db import models


class Atualizacao(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='arquivos_atualizacao', null=True, blank=True)

    def __str__(self):
        return 'Atualixação do dia {}'.format(self.data)

    class Meta:
        verbose_name = 'Atualização'
        verbose_name_plural = 'Atualizações'
