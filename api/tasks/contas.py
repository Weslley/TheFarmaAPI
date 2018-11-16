# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-05 09:22:47
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-11 11:42:00

# from thefarmaapi._celery import app
from thefarmaapi._celery import app
from celery import shared_task

from api.models.pedido import Pedido
from api.models.conta import Conta
from api.models.enums import StatusPedido,\
	StatusPedidoFaturamento, StatusPagamento, \
	FormaPagamento, StatusPagamentoConta, StatusConta

from datetime import date, timedelta


def get_faturamento(data_pedido, farmacia):
	delay_faturamento = timedelta(days=10)
	dia_faturamento = farmacia.dia_faturamento

	data_ref_faturamento = data_pedido.replace(day=dia_faturamento)
	dt_limite_faturamento = data_ref_faturamento - delay_faturamento

	if dia_faturamento in range(11, 32):
		# Se o dia de faturamento esta entre 11 e 31

		if (data_pedido.day <= dt_limite_faturamento.day):
			# Se o dia do pedido for anterior ou igual ao dia de faturamento
			# o pedido sera referente ao faturamento do seu mes atual
			dt_faturamento = data_pedido.replace(day=dia_faturamento)

		else:
			# Se o dia do pedido for maior que dia de faturamento
			# o pedido sera referente ao faturamento do mes posterior
			dt_faturamento = data_pedido.replace(
				day=dia_faturamento, month=(data_pedido.month + 1)
			)

	else:
		# Se o dia de faturamento esta entre 1 e 10
		dt_faturamento = data_pedido.replace(
			day=dia_faturamento, month=(data_pedido.month + 1)
		)

	conta, created = Conta.objects.get_or_create(
		status=StatusPagamentoConta.ABERTA,
		farmacia=farmacia, data_vencimento=dt_faturamento
	)

	return conta


def faturar_pedido(pedido):
	farmacia = pedido.farmacia
	data_pedido = pedido.data_criacao

	faturamento = get_faturamento(data_pedido, farmacia)
	from pprint import pprint
	pprint(faturamento)

	# Se o pedido for no credito
	if pedido.forma_pagamento == FormaPagamento.CARTAO:
		faturamento.valor_total += pedido.liquido
	else:
		faturamento.valor_total -= pedido.valor_comissao_thefarma

	if faturamento.valor_total < 0:
		faturamento.tipo = StatusConta.PAGAR
	else:
		faturamento.tipo = StatusConta.RECEBER

	faturamento.save()

	pedido.status_faturamento = StatusPedidoFaturamento.FATURADO
	pedido.faturamento = faturamento
	pedido.save()


@shared_task
def faturamento():
	# print("fazer fatuarmento mensal")
	pedidos_nao_faturados = Pedido.objects.filter(
		# Q(data_criacao__gt=inicio_mes) | Q(data_criacao__lte=hoje),
		status_faturamento=StatusPedidoFaturamento.NAO_FATURADO,
		status_pagamento=StatusPagamento.PAGO,
		status=StatusPedido.ENTREGUE
	)

	# nf == pedido nao faturado
	if pedidos_nao_faturados.exists():
		for pedido_nf in pedidos_nao_faturados:
			faturar_pedido(pedido_nf)
