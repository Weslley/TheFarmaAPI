# -*- coding: utf-8 -*-
# @Author: caiovictormc
# @Date:   2018-10-08 09:27:10
# @Last Modified by:   caiovictormc
# @Last Modified time: 2018-10-08 09:27:53
from api.utils.enum import IntEnum


class StatusConta(IntEnum):
    """
    Status das Contas
    """
    RECEBER = 0
    PAGAR = 1
