from django.db import models

from datetime import datetime


def generate_filename(instance, filename):
    return 'boletos/{}'.format(filename)


class Boleto(models.Model):
    pdf = models.FileField(upload_to=generate_filename)
    codigo_de_barras = models.CharField(max_length=275, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        str_template = 'Boleto {}'
        try:
            if self.conta:
                return str_template.format(self.conta.id)
        except AttributeError as e:
            if self.data_atualizacao:
                return str_template.format(self.data_atualizacao.strftime('%d/%m/%Y'))
            return str_template.format(self.id)

    def save(self, *args, **kwargs):
        try:
            self.conta.data_emissao = datetime.now()
            self.conta.save()
        except AttributeError as e:
            pass
        finally:
            super().save(*args, **kwargs)
