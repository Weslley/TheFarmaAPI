from django.contrib.auth.models import User
from django.db import models

from api.utils import tipo_post


def generate_filename(self, filename):
    return 'usuarios/{0}/posts/{1}'.format(self.usuario.id, filename)


class Post(models.Model):
    titulo = models.CharField(max_length=60)
    imagem = models.ImageField(upload_to=generate_filename, blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    conteudo = models.TextField(blank=True, null=True)
    url_referencia = models.URLField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    tipo = models.IntegerField(choices=tipo_post.CHOICES, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def likes(self):
        return int(self.curtidas.count())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from datetime import datetime
        self.data_atualizacao = datetime.now()
        return super(Post, self).save(force_insert, force_update, using, update_fields)
