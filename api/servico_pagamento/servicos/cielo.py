from cieloApi3 import *
from decouple import config
from api.servico_pagamento.servicos.servico_abc import Servico
from api.servico_pagamento import tipo_servicos
from api.utils import erros_cielo, status_transacao_cartao_cielo
from api.utils.generics import print_exception

SANDBOX = config('CIELO_SANDBOX', default=False, cast=bool)
MERCHANT_ID = config('CIELO_MERCHANT_ID', default='')
MERCHANT_KEY = config('CIELO_MERCHANT_KEY', default='')

TRANSLATE_BRANDS = (
    ('VISA', 'Visa'),
    ('MASTER', 'Master'),
    ('AMERICAN', 'Amex'),
    ('ELO', 'Elo'),
    ('AURA', 'Aura'),
    ('JCB', 'JCB'),
    ('DINERS', 'Diners'),
    ('DISCOVER', 'Discover')
)


class ResponseCieloException(Exception):

    def __init__(self, erros=None, *args, **kwargs):
        self.erros = erros
        self.returned = kwargs if kwargs else None


    def __str__(self):
        erro = self.erros[0]
        for cod, value in erros_cielo.CHOICES:
            if cod == erro:
                return value

        return 'Erro inesperado.'


class ServicoCielo(Servico):

    @classmethod
    def realizar_pagamento(cls, data):
        data = cls.checkout_kwargs(data)
        return cls.pagar(data)

    @classmethod
    def realizar_cancelamento(cls, data):
        data = cls.checkout_cancelamento_kwargs(data)
        return cls.cancelar(data)

    @classmethod
    def checkout_kwargs(cls, kwargs):
        if 'token' not in kwargs:
            validade = kwargs['validade']
            mes, ano = validade.split('/')
            kwargs['validade'] = '{}/20{}'.format(mes.rjust(2, '0'), ano.rjust(2, '0'))

        for nome, valor in TRANSLATE_BRANDS:
            if nome == kwargs['bandeira']:
                kwargs['bandeira'] = valor
                break

        return kwargs

    @classmethod
    def checkout_cancelamento_kwargs(cls, kwargs):
        return kwargs

    @classmethod
    def validate_result(cls, data):
        return data

    @classmethod
    def pagar(cls, kwargs):
        json_venda = None
        json_captura = None
        try:
            # Crie uma instância de Sale
            sale = cls.load_sale(kwargs)

            # Valor da venda
            valor = centavos(kwargs['valor'])

            # Crie uma instância de Credit Card utilizando os dados de teste
            # esses dados estão disponíveis no manual de integração
            credit_card = cls.load_creditcard(kwargs)

            # Crie uma instância de Payment informando o valor do pagamento
            sale.payment = Payment(valor)
            sale.payment.credit_card = credit_card

            json_venda, payment_id, capturavel = cls.cria_venda(sale)
            if capturavel:
                json_captura = cls.captura_venda(payment_id, valor)

            return {'venda': json_venda, 'captura': json_captura}
        except Exception as err:
            print_exception()
            return {'venda': json_venda, 'captura': json_captura}
            # error_codes = get_codigo_erros(str(err))
            # if error_codes:
                # raise ResponseCieloException(error_codes, **{'venda': json_venda, 'captura': json_captura})
            # raise err

    @classmethod
    def status_pagamento(cls, payment_id):
        try:
            # Configurando o ambiente e configurando o merchant
            ambiente, merchant = cls.load_transacao()

            # Cria instância do controlador do ecommerce
            cielo_ecommerce = CieloEcommerce(merchant, ambiente)

            sale = cielo_ecommerce.get_sale(payment_id)

            return sale['Payment']['Status'] if 'Payment' in sale and 'Status' in sale['Payment'] else 0

        except Exception as err:
            error_codes = get_codigo_erros(str(err))
            if error_codes:
                raise ResponseCieloException(error_codes, **{'status': status})
            raise err

    @classmethod
    def cancelar(cls, kwargs):
        json_cancelamento = None
        payment_id, value  = kwargs['payment_id'], kwargs['valor']

        try:
            value = centavos(value)

            # Configurando o ambiente e configurando o merchant
            ambiente, merchant = cls.load_transacao()

            # Cria instância do controlador do ecommerce
            cielo_ecommerce = CieloEcommerce(merchant, ambiente)

            # Com o ID do pagamento, podemos fazer seu cancelamento
            json_cancelamento = cielo_ecommerce.cancel_sale(payment_id, value)

            return {'cancelamento': json_cancelamento}
        except Exception as err:
            error_codes = get_codigo_erros(str(err))
            if error_codes:
                raise ResponseCieloException(error_codes, **{'cancelamento': json_cancelamento})
            raise err

    @classmethod
    def tipo_servico(cls):
        return tipo_servicos.CIELO

    @classmethod
    def create_token(cls, validate_data):
        # Configure o ambiente
        environment = Environment(sandbox=SANDBOX)

        # Configure seu merchant, para gerar acesse: https://cadastrosandbox.cieloecommerce.cielo.com.br/
        merchant = Merchant(MERCHANT_ID, MERCHANT_KEY)

        # Crie uma instância de Credit Card utilizando os dados de teste
        # esses dados estão disponíveis no manual de integração)
        month = int(validate_data['mes_expiracao'])
        year = int(validate_data['ano_expiracao'])
        cliente = validate_data['cliente']
        customer_name = cliente.usuario.get_full_name() if cliente.usuario.get_full_name() else validate_data['nome_proprietario']

        credit_card = CreditCard(validate_data['cvv'], validate_data['bandeira'])
        credit_card.expiration_date = '{:02d}/{:d}'.format(month, year)
        credit_card.card_number = validate_data['numero_cartao']
        credit_card.holder = validate_data['nome_proprietario']
        credit_card.customer_name = customer_name

        # Cria instância do controlador do ecommerce
        cielo_ecommerce = CieloEcommerce(merchant, environment)

        # Criar a venda e imprime o retorno
        cielo_ecommerce.create_card_token(credit_card)

        # Com o cartão gerado token na Cielo, já temos o Token do cartão para uma futura cobrança
        return credit_card.card_token

    @classmethod
    def get_card_data(cls, card):
        customer = Customer(
            card.cliente.usuario.get_full_name() if card.cliente.usuario.get_full_name() else card.nome_proprietario
        )

        # Crie uma instância de Credit Card utilizando os dados de teste via token
        credit_card_token = CreditCard(card.cvv, card.bandeira)
        credit_card_token.card_token = card.token

        return customer, credit_card_token

    @classmethod
    def load_customer(cls, kwargs):
        return Customer('CLIENTE THEFARMA')

    @classmethod
    def load_transacao(cls):
        # Configurando o ambiente
        ambiente = Environment(sandbox=SANDBOX)

        # Configure seu merchant
        merchant = Merchant(MERCHANT_ID, MERCHANT_KEY)

        return ambiente, merchant

    @classmethod
    def load_creditcard(cls, kwargs):
        credit_card = CreditCard(kwargs['cvv'], kwargs['bandeira'])
        if 'token' in kwargs:
            credit_card.card_token = kwargs['token']
            return credit_card

        credit_card.expiration_date = kwargs['validade']
        credit_card.card_number = kwargs['numero_cartao']
        return credit_card

    @classmethod
    def load_sale(cls, kwargs):
        # Crie uma instância de Sale informando o ID do pagamento
        sale = Sale(kwargs['pedido_id'])

        # Crie uma instância de Customer informando o nome do cliente
        sale.customer = cls.load_customer(kwargs)

        return sale

    @classmethod
    def cria_venda(cls, sale):
        capturavel = False

        # Configurando o ambiente e configurando o merchant
        ambiente, merchant = cls.load_transacao()

        # Cria instância do controlador do ecommerce
        cielo_ecommerce = CieloEcommerce(merchant, ambiente)

        # Criar a venda e imprime o retorno
        response_create_sale = cielo_ecommerce.create_sale(sale)

        payment_id = sale.payment.payment_id

        capturavel = response_create_sale['Payment']['Status'] == status_transacao_cartao_cielo.AUTHORIZED

        return response_create_sale, payment_id, capturavel

    @classmethod
    def captura_venda(cls, payment_id, value):
        # Configurando o ambiente e configurando o merchant
        ambiente, merchant = cls.load_transacao()

        # Cria instância do controlador do ecommerce
        cielo_ecommerce = CieloEcommerce(merchant, ambiente)

        # Com o ID do pagamento, podemos fazer sua captura,
        # se ela não tiver sido capturada ainda
        response_capture_sale = cielo_ecommerce.capture_sale(payment_id, value, 0)

        return response_capture_sale


def centavos(valor):
    return int(round(valor, 2) * 100)

def get_codigo_erros(exception_error):
    try:
        import re
        regex = r'\[([0-9]+)\]'
        matches = re.finditer(regex, exception_error)
        _data = []
        for m in matches:
            cod = m.group().replace('[','').replace(']', '')
            cod = int(cod)
            _data.append(cod)

        return _data
    except:
        return None
