"""
Métodos para geração de códigos SMS para login
"""
from pyzenvia import Sender
from api.models.configuracao import Configuracao


def generate_code(user):
    """
    :param user: Usuário<User>
    Método para gerar código para ser utilizado na validação do SMS
    :return: str
    """
    return '{}{}'.format(
        sum([int(digit) for digit in str(user.cliente.celular if user.cliente.celular else '99')]),
        str((user.last_login if user.last_login else user.date_joined).timestamp()).split('.')[0][-2:]
    )


def check_code(user, sms_code):
    """
    Método para verificar código SMS enviado.
    :return: bool
    """
    return generate_code(user) == str(sms_code)


def send_sms_code(user):
    """Método para enviar sms code"""
    try:
        conf = Configuracao.objects.first()
        if not conf:
            conf = Configuracao.objects.create()

        sender = Sender(conf.zenvia_conta, conf.zenvia_password)

        data = {
            "phone": '55{}'.format(user.cliente.celular),
            "message": 'Codigo: {}'.format(generate_code(user)),
            "from": 'TheFarma'
        }
        response = sender.send(**data)
        print(response)
        return response
    except Exception as err:
        print(err)
        return None
