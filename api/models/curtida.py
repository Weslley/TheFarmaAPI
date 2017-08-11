from django.db import models
from django.contrib.auth.models import User

from api.models.post import Post


class Curtida(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='curtidas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')

    class Meta:
        unique_together = ('post', 'usuario')
