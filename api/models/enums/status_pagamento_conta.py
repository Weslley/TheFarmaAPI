# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-08 10:07:37
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-11 09:52:40

from api.utils.enum import IntEnum


class StatusPagamentoConta(IntEnum):
    """
    Status de contas a receber
    """
    ABERTA = 0
    PAGA = 1
    ATRASADA = 2
    CANCELADA = 3
