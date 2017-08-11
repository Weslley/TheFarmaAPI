from datetime import datetime

from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator

from api.models.log import Log
from api.models.enums import (
    StatusItem,
    StatusPedido,
    FormaPagamento,
    StatusItemProposta,
    StatusPagamentoCartao
)
from api.models.bairro import Bairro
from api.models.cartao import Cartao
from api.models.cidade import Cidade
from api.models.cliente import Cliente
from api.models.farmacia import Farmacia
from api.models.apresentacao import Apresentacao


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
    cidade = models.CharField(max_length=150)
    uf = models.CharField(max_length=2)
    bairro = models.CharField(max_length=60)
    nome_endereco = models.CharField(max_length=40)
    nome_destinatario = models.CharField(max_length=80, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    delivery = models.BooleanField(default=True)
    troco = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return 'Pedido {}'.format(self.id)

    @property
    def valor_bruto(self):
        resultado = self.contas_receber_farmacia.aggregate(valor_bruto=Sum('valor_bruto'))
        return resultado['valor_bruto']

    @property
    def valor_liquido(self):
        resultado = self.contas_receber_farmacia.aggregate(valor_liquido=Sum(
            F('valor_bruto') - F('valor_administradora_cartao') - F('valor_thefarma') - F('valor_adiantamento')
        ))
        return resultado['valor_liquido']

    @property
    def propostas(self):
        """
        Property que retorna todas as propostas
        :return:
        """
        farmacias = [item.farmacia for item in self.itens_proposta.select_related('farmacia').distinct('farmacia')]
        return [
            {
                'farmacia': farmacia,
                'itens': farmacia.get_itens_proposta(self),
                'status': farmacia.get_status_proposta(self),
                'valor_total': farmacia.get_valor_proposta(self)
            }
            for farmacia in farmacias
        ]

    @property
    def cidade_obj(self):
        """
        Property de cidade, retorna o objeto baseado nos dados do pedido
        :return:
        """
        qs = Cidade.objects.filter(nome__exact=self.cidade, uf__sigla=self.uf)
        if qs.exists():
            return qs.first()
        return None


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.log:
            self.log.data_criacao = datetime.now()
            self.log.save(using=using)
        return super(Pedido, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_vendidos')
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    farmacia = models.ForeignKey(Farmacia, null=True, related_name='apresentacoes_vendidos')
    status = models.IntegerField(choices=StatusItem.choices(), default=StatusItem.ABERTO)

    class Meta:
        unique_together = ('pedido', 'apresentacao', 'farmacia')


class PagamentoCartao(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='cartoes')
    cartao = models.ForeignKey(Cartao, related_name='pagamentos')
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.IntegerField(choices=StatusPagamentoCartao.choices(), default=StatusPagamentoCartao.IDENTIFICACAO)


class ItemPropostaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens_proposta')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_propostos')
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    farmacia = models.ForeignKey(Farmacia, related_name='itens_proposta')
    status = models.IntegerField(choices=StatusItemProposta.choices(), default=StatusItemProposta.ABERTO)
    possui = models.BooleanField(default=True)

    class Meta:
        unique_together = ('pedido', 'apresentacao', 'farmacia')
