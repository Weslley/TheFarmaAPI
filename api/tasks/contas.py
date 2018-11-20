# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-05 09:22:47
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-11 11:42:00

from django.db.models import Q

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
	dia_pagamento = farmacia.dia_pagamento

	data_ref_pagamento = data_pedido.replace(day=dia_pagamento)

	dt_limite_faturamento = data_ref_pagamento - delay_faturamento

	if dia_pagamento in range(11, 32):
		# Se o dia de faturamento esta entre 11 e 31

		if (data_pedido.day <= dt_limite_faturamento.day):
			# Se o dia do pedido for anterior ou igual ao dia de faturamento
			# o pedido sera referente ao faturamento do seu mes atual
			dt_vencimento = data_pedido.replace(day=dia_pagamento)

		else:
			# Se o dia do pedido for maior que dia de faturamento
			# o pedido sera referente ao faturamento do mes posterior
			dt_vencimento = data_pedido.replace(
				day=dia_pagamento, month=(data_pedido.month + 1)
			)

	else:
		# Se o dia de faturamento esta entre 1 e 10
		dt_vencimento = data_pedido.replace(
			day=dia_pagamento, month=(data_pedido.month + 1)
		)

	dt_faturamento = dt_vencimento - delay_faturamento
	conta, created = Conta.objects.get_or_create(
		status=StatusPagamentoConta.ABERTA, farmacia=farmacia, 
		data_vencimento=dt_vencimento, data_faturamento=dt_faturamento
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
		faturamento.valor_total += pedido.valor_liquido
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
	pedidos_nao_faturados = Pedido.objects.filter(
		status_faturamento=StatusPedidoFaturamento.NAO_FATURADO,
		status_pagamento=StatusPagamento.PAGO,
		status=StatusPedido.ENTREGUE
	)

	# nf == pedido nao faturado
	if pedidos_nao_faturados.exists():
		for pedido_nf in pedidos_nao_faturados:
			faturar_pedido(pedido_nf)

@shared_task
def alterar_status_contas():
	today = date.today()
	
	# Fechar contas que passaram do faturamento
	contas_a_fechar = Conta.objects.filter(status=StatusPagamentoConta.ABERTA)
	for conta_a_fechar in contas_a_fechar:
		if conta_a_fechar.data_faturamento:
			if conta_a_fechar.data_faturamento <= today:
				conta_aberta.status = StatusPagamentoConta.FECHADA
				conta_aberta.save()


	# Vencer contas abertas que passaram do vencimento
	contas_abertas = Conta.objects.filter(
		Q(status=StatusPagamentoConta.ABERTA) | Q(status=StatusPagamentoConta.FECHADA)
	)
	for conta_aberta in contas_abertas:
		if conta_aberta.data_vencimento <= today:
			conta_aberta.status = StatusPagamentoConta.ATRASADA
			conta_aberta.save()
