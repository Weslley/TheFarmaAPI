from django.db import models
from django.contrib.auth.models import User
from misc.validators import validate_file_extension


class Atualizacao(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='arquivos_atualizacao', null=True, blank=True, validators=[validate_file_extension])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Atualização do dia {}'.format(self.data)

    class Meta:
        verbose_name = 'Atualização'
        verbose_name_plural = 'Atualizações'
        ordering = ['-id', ]
