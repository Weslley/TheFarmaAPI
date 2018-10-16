# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-08 09:00:09
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-11 11:34:06

from django.db import models

from api.models.enums import StatusConta, StatusPagamentoConta
from api.models.farmacia import Farmacia


class Conta(models.Model):
	"""
	Conta em relacao ao TheFarma, tipo PAGAR significa
	TheFarma pagar a farmacia
	"""
	data_criacao = models.DateTimeField(auto_now_add=True)
	data_atualizacao = models.DateTimeField(auto_now=True)
	farmacia = models.ForeignKey(Farmacia, related_name='contas')

	status = models.IntegerField(
		choices=StatusPagamentoConta.choices(),
		default=StatusPagamentoConta.ABERTA
	)

	tipo = models.IntegerField(
		choices=StatusConta.choices(),
		default=StatusConta.PAGAR
	)

	data_vencimento = models.DateField(null=True, blank=True)
	valor_total = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )

	def __str__(self):
		return "{}".format(self.farmacia.razao_social)
