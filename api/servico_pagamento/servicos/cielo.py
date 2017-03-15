from cieloApi3 import *
import json
from decouple import config
from api.servico_pagamento.servicos.servico_abc import Servico
from api.servico_pagamento import tipo_servicos

SANDBOX = config('CIELO_SANDBOX', default=False, cast=bool)
MERCHANT_ID = config('CIELO_MERCHANT_ID', default='')
MERCHANT_KEY = config('CIELO_MERCHANT_KEY', default='')


class ServicoCielo(Servico):

    @classmethod
    def realizar_pagamento(cls, **kwargs):
        return True

    @classmethod
    def tipo_servico(cls):
        return tipo_servicos.CIELO
