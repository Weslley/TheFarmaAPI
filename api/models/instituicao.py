from django.contrib.auth.models import User
from django.db import models


class Instituicao(models.Model):
    razao_social = models.CharField(max_length=120)
    nome_fantasia = models.CharField(max_length=70)
    cpf_cnpj = models.CharField(verbose_name='CPF/CNPJ', max_length=14)
    site = models.URLField()
    logo = models.ImageField(upload_to='instituicoes')
    telefone = models.CharField(max_length=11)
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        verbose_name = 'Instituição'

    def __str__(self):
        return self.nome_fantasia


class UsuarioInstituicao(models.Model):
    instituicao = models.ForeignKey(Instituicao, related_name='usuarios')
    user = models.OneToOneField(User, related_name='user_instituicao')

    class Meta:
        unique_together = ('instituicao', 'user')
