from django.db import models
from django.contrib.auth.models import User

from api.utils import sexo
from api.models.endereco import Endereco


def generate_filename(self, filename):
    return 'usuarios/{0}/perfil/{1}'.format(self.usuario.id, filename)


class Cliente(models.Model):
    sexo = models.CharField(max_length=1, choices=sexo.CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to=generate_filename, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField(blank=True, null=True)
    celular = models.CharField(max_length=11, null=True, blank=True, unique=True)
    cpf = models.CharField(max_length=11, null=True, blank=False, unique=True)
    telefone = models.CharField(max_length=11, null=True, blank=False, unique=True)
    email_confirmado = models.BooleanField(default=False)


class ClienteEndereco(models.Model):
    _cliente = models.ForeignKey(Cliente, related_name='enderecos')
    endereco = models.OneToOneField(Endereco)

    class Meta:
        unique_together = ('_cliente', 'endereco')
