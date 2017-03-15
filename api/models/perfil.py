from django.contrib.auth.models import User
from django.db import models
from api.utils import sexo


def generate_filename(self, filename):
    return 'usuarios/{0}/perfil/{1}'.format(self.usuario.id, filename)


class Perfil(models.Model):
    sexo = models.CharField(max_length=1, choices=sexo.CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to=generate_filename, blank=True, null=True)
    sobre = models.TextField(blank=True, null=True)
    facebook_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField(blank=True, null=True)
    """
    cpf
    telefone
    """
