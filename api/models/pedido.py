from django.db import models

from api.models.apresentacao import Apresentacao
from api.models.bairro import Bairro
from api.models.cartao import Cartao
from api.models.cidade import Cidade
from api.models.cliente import Cliente
from api.models.farmacia import Farmacia
from api.models.log import Log
from django.core.validators import MinValueValidator
from api.models.enums import FormaPagamento, StatusPedido, StatusPagamentoCartao, StatusItem


class Pedido(models.Model):
    valor_frete = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    numero_parcelas = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    cliente = models.ForeignKey(Cliente)
    status = models.IntegerField(default=StatusPedido.ABERTO, choices=StatusPedido.choices())
    log = models.OneToOneField(Log)
    forma_pagamento = models.IntegerField(choices=FormaPagamento.choices(), default=FormaPagamento.CARTAO)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=80)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, related_name='enderecos_pedido')
    bairro = models.ForeignKey(Bairro, related_name='enderecos_pedido')
    nome_endereco = models.CharField(max_length=40)
    nome_destinatario = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return 'Pedido {}'.format(self.id)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_vendidos')  # Não entendi por seria uma lista
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    farmacia = models.ForeignKey(Farmacia)
    status = models.IntegerField(choices=StatusItem.choices(), default=StatusItem.ABERTO)


class PagamentoCartao(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='cartoes')
    cartao = models.ForeignKey(Cartao, related_name='pagamentos')
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.IntegerField(choices=StatusPagamentoCartao.choices(), default=StatusPagamentoCartao.IDENTIFICACAO)
