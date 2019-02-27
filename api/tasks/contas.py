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

from datetime import date, timedelta,datetime


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
			try:
				dt_vencimento = data_pedido.replace(
					day=dia_pagamento, month=(data_pedido.month + 1)
				)
			except:
				if data_pedido.month == 12:
					dt_vencimento = data_pedido.replace(
						day=dia_pagamento, month=1, year=(data_pedido.year + 1)
					)
				else:
					raise Exception('Erro ao gerar a data do faturamento')
	else:
		# Se o dia de faturamento esta entre 1 e 10
		try:
			dt_vencimento = data_pedido.replace(
				day=dia_pagamento, month=(data_pedido.month + 1)
			)
		except:
			if data_pedido.month == 12:
				dt_vencimento = data_pedido.replace(
					day=dia_pagamento, month=1, year=(data_pedido.year + 1)
				)
			else:
				raise Exception('Erro ao gerar a data do faturamento')

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
				conta_a_fechar.status = StatusPagamentoConta.FECHADA
				conta_a_fechar.save()

	# Vencer contas abertas que passaram do vencimento
	contas_abertas = Conta.objects.filter(
		Q(status=StatusPagamentoConta.ABERTA) | Q(status=StatusPagamentoConta.FECHADA)
	)
	for conta_aberta in contas_abertas:
		if conta_aberta.data_vencimento < today:
			conta_aberta.status = StatusPagamentoConta.ATRASADA
			conta_aberta.save()

def get_faturamento_pedido(pedido):
	"""
	Recupera o faturamento de um pedido
	pedido: Pedido
	return: Conta
	"""
	#init vars
	DIA_FATURA = 20
	DIA_PAGAMENTO = 1
	data_pedido = datetime.now()
	#cria a data da fatrua
	data_faturamento = datetime(data_pedido.year,data_pedido.month,DIA_FATURA)
	#passa o vencimento para o proximo mes dia 1
	if data_pedido.month == 12:
		#passa para o proximo ano
		data_vencimento = datetime(data_pedido.year+1,1,DIA_PAGAMENTO)
	else:
		data_vencimento = datetime(data_pedido.year,data_pedido.month+1,DIA_PAGAMENTO)
	#cria ou recupera o faturamento aberto
	conta, created = Conta.objects.get_or_create(
		status=StatusPagamentoConta.ABERTA,
		farmacia=pedido.farmacia,
		data_vencimento=data_vencimento,
		data_faturamento=data_faturamento
	)
	return conta

def processa_pedido(pedido):
	"""
	Metodo responsavel por fazer o faturamento do pedido
	pedido: Pedido
	return:
	"""
	conta = get_faturamento_pedido(pedido)
	# Se o pedido for no credito
	if pedido.forma_pagamento == FormaPagamento.CARTAO:
		conta.valor_total += pedido.valor_liquido
	else:
		conta.valor_total -= pedido.valor_comissao_thefarma

	if conta.valor_total < 0:
		conta.tipo = StatusConta.PAGAR
	else:
		conta.tipo = StatusConta.RECEBER

	conta.save()
	pedido.status_faturamento = StatusPedidoFaturamento.FATURADO
	pedido.faturamento = faturamento
	pedido.save()

@shared_task
def faturar_pedidos():
	#todos os pedidos que nao foram faturados
	pedidos_nao_faturados = Pedido.objects.filter(
		status_faturamento=StatusPedidoFaturamento.NAO_FATURADO,
		status_pagamento=StatusPagamento.PAGO,
		status=StatusPedido.ENTREGUE
	)

	#processa todos os pedidos nao faturados
	for item in pedidos_nao_faturados:
		processa_pedido(item)