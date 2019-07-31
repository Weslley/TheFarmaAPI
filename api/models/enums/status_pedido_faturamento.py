# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-11 09:58:36
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-11 10:08:33
from api.utils.enum import IntEnum


class StatusPedidoFaturamento(IntEnum):
    """
    Status das Contas
    """
    NAO_FATURADO = 0
    FATURADO = 1
