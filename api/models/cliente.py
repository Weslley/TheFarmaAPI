import urllib.request
import os

from django.contrib.auth.models import User
from django.core.files.base import File
from django.db import models

from api.models.endereco import Endereco
from api.utils import sexo


def generate_filename(self, filename):
    return 'usuarios/{0}/perfil/{1}'.format(self.usuario.id, filename)


class Cliente(models.Model):
    sexo = models.CharField(max_length=1, choices=sexo.CHOICES, blank=True, null=True, default=None)
    foto = models.ImageField(upload_to=generate_filename, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    data_nascimento = models.DateField(blank=True, null=True)
    celular = models.CharField(max_length=11, null=True, blank=True, unique=True)
    cpf = models.CharField(max_length=11, null=True, blank=False, unique=True)
    email_confirmado = models.BooleanField(default=False)
    celular_confirmado = models.BooleanField(default=False)
    fcm_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.usuario.get_full_name()

    @property
    def celular_formatado(self):
        if self.celular:
            if len(self.celular)==11:
                return '({}{}) {}{}{}{}{}-{}{}{}{}'.format(*re.sub("\D",'', self.celular))
            elif len(self.celular)==1:
                return '({}{}) {}{}{}{}-{}{}{}{}'.format(*re.sub("\D",'', self.celular))

        return re.sub('\D','', self.celular)

    def get_remote_image(self, image_url):
        """
        Metodo para fazer o download e da imagem da url e salvar no campo foto
        :param image_url: URL da imagem
        :return:
        """
        if image_url:
            foto_antiga = None
            if self.foto:
                foto_antiga = self.foto.path

            extension = None
            for e in ['.jpg', '.jpeg', '.png']:
                if e in image_url:
                    extension = e

            if extension:
                result = urllib.request.urlretrieve(image_url)
                filename = '{}{}'.format(os.path.basename(image_url)[:5], extension)
                self.foto.save(
                    filename,
                    File(open(result[0], 'rb'))
                )
                self.save()

                if foto_antiga:
                    os.remove(foto_antiga)


class ClienteEndereco(models.Model):
    _cliente = models.ForeignKey(Cliente, related_name='enderecos')
    endereco = models.OneToOneField(Endereco)

    class Meta:
        unique_together = ('_cliente', 'endereco')
