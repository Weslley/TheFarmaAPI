from datetime import datetime

from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum

from api.models.administradora import Administradora
from api.models.apresentacao import Apresentacao
from api.models.cartao import Cartao
from api.models.cidade import Cidade
from api.models.cliente import Cliente
from api.models.conta import Conta
from api.models.enums import (FormaPagamento, StatusItem, StatusItemProposta,
                              StatusPagamentoCartao, StatusPedido)
from api.models.enums.status_pagamento import StatusPagamento
from api.models.enums.tipo_produto import TipoProduto
from api.models.enums.status_pedido_faturamento import StatusPedidoFaturamento
from api.models.farmacia import Farmacia
from api.models.log import Log
from django.contrib.postgres.fields import JSONField

from api.utils.math import truncate


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    farmacia = models.ForeignKey(Farmacia, null=True, related_name='pedidos')
    log = models.OneToOneField(Log)
    data_atualizacao = models.DateTimeField(auto_now=True,blank=True,null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_faturamento = models.DateTimeField(null=True, blank=True)
    status_faturamento = models.IntegerField(
        choices=StatusPedidoFaturamento.choices(),
        default=StatusPedidoFaturamento.NAO_FATURADO,
        null=True
    )
    faturamento = models.ForeignKey(
        Conta, on_delete=models.SET_NULL, related_name='pedidos',
        null=True, blank=True
    )

    views = models.IntegerField(default=0, null=True, blank=True)

    delivery = models.BooleanField(default=True)
    valor_frete = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    valor_bruto_sem_frete = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        null=True, blank=True,
        validators=[MinValueValidator(0), ]
    )
    valor_bruto = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        validators=[MinValueValidator(0), ]
    )
    valor_liquido = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, 
        validators=[MinValueValidator(0), ]
    )
    valor_comissao_administradora = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, 
        validators=[MinValueValidator(0), ]
    )
    valor_comissao_thefarma = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, 
        validators=[MinValueValidator(0), ]
    )
    troco = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, 
        validators=[MinValueValidator(0), ]
    )
    numero_parcelas = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), ]
    )
    status = models.IntegerField(
        default=StatusPedido.ABERTO, choices=StatusPedido.choices()
    )
    status_pagamento = models.IntegerField(
        choices=StatusPagamento.choices(), default=StatusPagamento.ABERTO
    )
    forma_pagamento = models.IntegerField(
        choices=FormaPagamento.choices(), default=FormaPagamento.CARTAO
    )
    status_cartao = models.IntegerField(
        choices=StatusPagamentoCartao.choices(), 
        default=StatusPagamentoCartao.NAO_FINALIZADO
    )

    cep = models.CharField(max_length=8, null=True, blank=True)
    logradouro = models.CharField(max_length=80, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    bairro = models.CharField(max_length=150, null=True, blank=True)
    nome_endereco = models.CharField(max_length=40, null=True, blank=True)
    nome_destinatario = models.CharField(max_length=80, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    cartao = models.ForeignKey(Cartao, related_name='pedidos', null=True)
    administradora_cartao = models.ForeignKey(
        Administradora, null=True, 
        related_name='pedidos_pagos'
    )
    
    json_venda = JSONField(null=True)
    json_captura = JSONField(null=True)
    pagamento_status = models.IntegerField(null=True, blank=True)
    captura_status = models.IntegerField(null=True, blank=True)

    farmacias_receberam = models.CharField(null=True,blank=True,max_length=200)

    def __str__(self):
        return 'Pedido {}'.format(self.id)

    def get_status_submissao(self, farmacia):
        return farmacia.get_status_proposta(self).value

    @property
    def comissao_thefarma(self):
        """
        Property para retornar comissão de acordo com os itens e os percentuais da farmacia
        :return:
        """
        comissao = 0

        if self.farmacia:
            for item in self.itens.filter(status=StatusItem.CONFIRMADO):
                comissao += item.comissao

        return round(Decimal(comissao), 2)

    @property
    def comissao(self):
        """
        Property para calcular o valor da comissão por parcela e a diferença da primeira
        :return: Uma tupla (comissão, diferença)
        """
        comissao_base = self.comissao_thefarma
        comissao_parcela = truncate(comissao_base / self.numero_parcelas, 2)
        diff = 0
        if truncate(comissao_parcela * self.numero_parcelas, 2) < comissao_base:
            diff = truncate(float(comissao_base) - truncate(comissao_parcela * self.numero_parcelas, 2), 2)

        return comissao_parcela, diff

    @property
    def localizacao(self):
        """
        Localização do pedido
        :return: tupla de latitude e longitude
        """
        return self.latitude, self.longitude

    # @property
    # def valor_bruto(self):
    #     from decimal import Decimal
    #     valor = Decimal()
    #     for contas in self.contas_receber.all():
    #         valor += contas.valor_parcela
    #     return valor

    # @property
    # def valor_administradora_cartao(self):
    #     from decimal import Decimal
    #     valor = Decimal()
    #     for contas in self.contas_receber.all():
    #         valor += contas.valor_administradora_cartao
    #     return valor
    

    # @property
    # def valor_liquido(self):
    #     resultado = self.contas_receber.aggregate(valor_liquido=Sum(
    #         self.valor_bruto - self.valor_administradora_cartao - F('valor_thefarma') - F('valor_adiantamento')
    #     ))
    #     return resultado['valor_liquido']

    @property
    def propostas(self):
        """
        Property que retorna todas as propostas
        :return:
        """
        return [
            {
                'farmacia': farmacia,
                'possui_todos_itens': farmacia.possui_todos_itens(self),
                'itens': farmacia.get_itens_proposta(self),
                'status': farmacia.get_status_proposta(self),
                'valor_total': farmacia.get_valor_proposta(self),
                'valor_frete': farmacia.get_valor_frete(self),
                'valor_total_com_frete': farmacia.get_valor_proposta_com_frete(self),
                'quantidade_maxima_parcelas': farmacia.get_quantidade_maxima_parcelas(self)
            }
            for farmacia in self.farmacias
        ]

    @property
    def farmacias(self):
        return [item.farmacia for item in self.itens_proposta.select_related('farmacia').distinct('farmacia')]

    @property
    def cidade_obj(self):
        """
        Property de cidade, retorna o objeto baseado nos dados do pedido
        :return:
        """
        qs = Cidade.objects.filter(nome__exact=self.cidade, uf__sigla=self.uf)
        if qs.exists():
            return qs.first()

        qs = Cidade.objects.filter(uf__sigla=self.uf)
        if qs.exists():
            return qs.first()

        return None

    def farmacia_esta_nas_propostas(self, farmacia):
        """
        Metodo que retorna se a farmacia esta entra as farmacias que fizeram propostas
        :param farmacia: Farmacia a ser verificada
        :return: Booleano informando se a farmacia esta ou não nas propostas
        """
        farmacias = [item.farmacia for item in self.itens_proposta.select_related('farmacia').distinct('farmacia')]
        return farmacia in farmacias

    def gerar_proposta(self, farmacias):
        if type(farmacias) == Farmacia:
            for item in self.itens.all():
                ItemPropostaPedido.objects.create(
                    pedido=self,
                    valor_unitario=item.valor_unitario,
                    quantidade=item.quantidade,
                    apresentacao=item.apresentacao,
                    farmacia=farmacias
                )
        elif type(farmacias) == list:
            for farmacia in farmacias:
                for item in self.itens.all():
                    if not ItemPropostaPedido.objects.filter(
                            pedido=self, farmacia=farmacia, apresentacao=item.apresentacao
                        ).exists():
                        ItemPropostaPedido.objects.create(
                            pedido=self,
                            valor_unitario=item.valor_unitario,
                            quantidade=item.quantidade,
                            apresentacao=item.apresentacao,
                            farmacia=farmacia
                        )

    def get_total_farmacia(self, farmacia_id):
        valor = 0
        for item in self.itens_proposta.filter(farmacia_id=farmacia_id, possui=True):
            valor += item.quantidade * item.valor_unitario
        return valor

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.log:
            self.log.data_atualizacao = datetime.now()
            self.log.save(using=using)
        return super(Pedido, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_vendidos')
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    quantidade_atendida = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), ])
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.IntegerField(choices=StatusItem.choices(), default=StatusItem.ABERTO)
    percentual_similar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_generico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_etico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_nao_medicamentos = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        unique_together = ('pedido', 'apresentacao')

    @property
    def total_bruto(self):
        return self.quantidade * self.valor_unitario

    @property
    def total_liquido(self):
        return self.quantidade_atendida * self.valor_unitario

    @property
    def farmacia(self):
        if self.pedido.farmacia:
            return self.pedido.farmacia
        return None

    @property
    def tipo(self):
        return self.apresentacao.produto.tipo

    @property
    def comissao(self):
        """
        :return:
        """
        valor = 0
        if self.farmacia:
            if self.tipo == TipoProduto.ETICO:
                valor = (self.percentual_etico * self.total_liquido) / 100
            elif self.tipo == TipoProduto.GENERICO:
                valor = (self.percentual_generico * self.total_liquido) / 100
            elif self.tipo == TipoProduto.SIMILAR:
                valor = (self.percentual_similar * self.total_liquido) / 100
            else:
                valor = (self.percentual_nao_medicamentos * self.total_liquido) / 100
        return valor


class ItemPropostaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens_proposta')
    apresentacao = models.ForeignKey(Apresentacao, related_name='itens_propostos')
    quantidade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), ])
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    farmacia = models.ForeignKey(Farmacia, related_name='itens_proposta')
    status = models.IntegerField(choices=StatusItemProposta.choices(), default=StatusItemProposta.ABERTO)
    possui = models.BooleanField(default=False)
    permutacao_id = models.IntegerField(default=0)


    @property
    def quantidade_inferior(self):
        """
        Property para informar se a quantidade deste item é inferior a solicitada
        :return:
        """
        return self.quantidade < self.pedido.itens.get(apresentacao=self.apresentacao).quantidade

    @ProcessLookupError
    def valor_proposta(self):
        return self.quantidade * self.valor_unitario

class LogData(models.Model):
    mes = models.CharField(max_length=75)
    ano = models.IntegerField()
    farmacia = models.ForeignKey(
        Farmacia, null=True, related_name='logs_pedidos'
    )

    def __str__(self):
        return '{} {}'.format(self.mes, self.ano)
