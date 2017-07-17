from django.contrib.auth.models import User
from django.db import models


class Parceiro(models.Model):
    razao_social = models.CharField(max_length=120)
    nome_fantasia = models.CharField(max_length=70)
    cpf_cnpj = models.CharField(verbose_name='CPF/CNPJ', max_length=14)
    site = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='parceiros', null=True, blank=True)
    telefone = models.CharField(max_length=11)
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        verbose_name = 'Parceiro'

    def __str__(self):
        return self.nome_fantasia


class UsuarioParceiro(models.Model):
    parceiro = models.ForeignKey(Parceiro, related_name='usuarios')
    usuario = models.OneToOneField(User, related_name='user_instituicao')

    class Meta:
        unique_together = ('parceiro', 'usuario')
