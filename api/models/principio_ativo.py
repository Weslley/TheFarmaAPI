from django.db import models


class PrincipioAtivo(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Princípio ativo'
        verbose_name_plural = 'Princípios ativo'

    def __str__(self):
        return '{}'.format(self.nome if self.nome else self.id)
