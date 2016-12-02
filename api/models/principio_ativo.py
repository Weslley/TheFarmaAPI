from django.db import models


class PrincipioAtivo(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Princípio ativo'
        verbose_name_plural = 'Princípios ativo'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.id)
