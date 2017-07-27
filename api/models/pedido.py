from django.db import models

from api.models.apresentacao import Apresentacao
from api.models.cartao import Cartao
from api.models.cliente import Cliente
from api.models.endereco import Endereco
from api.models.farmacia import Farmacia
from django.core.validators import MinValueValidator
from api.utils import status_pedido


class Pedido(models.Model):
    valor_frete = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    numero_parcelas = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    cliente = models.ForeignKey(Cliente, null=True)
    endereco = models.ForeignKey(Endereco, null=True)
    cartao = models.ForeignKey(Cartao, null=True)
    status = models.IntegerField(default=status_pedido.IDENTIFICACAO, choices=status_pedido.CHOICES)
    remote_ip = models.GenericIPAddressField()
    browser = models.CharField(max_length=50)

    def __str__(self):
        return 'Pedido {}'.format(self.id)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_vendidos')
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    farmacia = models.ForeignKey(Farmacia)
