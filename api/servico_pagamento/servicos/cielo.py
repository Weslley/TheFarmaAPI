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
        cls.checkout_kwargs(kwargs)
        return cls.pagar(kwargs)

    @classmethod
    def checkout_kwargs(cls, kwargs):
        pass

    @classmethod
    def pagar(cls, kwargs):
        # Configurando o ambiente
        ambiente = Environment(sandbox=SANDBOX)

        # Configure seu merchant
        merchant = Merchant(MERCHANT_ID, MERCHANT_KEY)

        # Crie uma instância de Sale informando o ID do pagamento
        sale = Sale('123')

        # Crie uma instância de Customer informando o nome do cliente
        sale.customer = Customer('Fulano de Tal')

        # Crie uma instância de Credit Card utilizando os dados de teste
        # esses dados estão disponíveis no manual de integração
        credit_card = CreditCard('123', 'Visa')
        credit_card.expiration_date = '12/2018'
        credit_card.card_number = '0000000000000001'
        credit_card.holder = 'Fulano de Tal'

        # Crie uma instância de Payment informando o valor do pagamento
        sale.payment = Payment(15700)
        sale.payment.credit_card = credit_card

        # Cria instância do controlador do ecommerce
        cielo_ecommerce = CieloEcommerce(merchant, ambiente)

        # Criar a venda e imprime o retorno
        response_create_sale = cielo_ecommerce.create_sale(sale)
        print('----------------------response_create_sale----------------------')
        print(json.dumps(response_create_sale, indent=2))
        print('----------------------response_create_sale----------------------')

        # Com a venda criada na Cielo, já temos o ID do pagamento, TID e demais
        # dados retornados pela Cielo
        payment_id = sale.payment.payment_id

        # Com o ID do pagamento, podemos fazer sua captura,
        # se ela não tiver sido capturada ainda
        response_capture_sale = cielo_ecommerce.capture_sale(payment_id, 15700, 0)
        print('----------------------response_capture_sale----------------------')
        print(json.dumps(response_capture_sale, indent=2))
        print('----------------------response_capture_sale----------------------')

        # E também podemos fazer seu cancelamento, se for o caso
        response_cancel_sale = cielo_ecommerce.cancel_sale(payment_id, 15700)
        print('---------------------response_cancel_sale---------------------')
        print(json.dumps(response_cancel_sale, indent=2))
        print('---------------------response_cancel_sale---------------------')
        return True

    @classmethod
    def tipo_servico(cls):
        return tipo_servicos.CIELO
