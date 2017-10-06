from api.mixins.consumers import BaseConsumer
from api.models.farmacia import Farmacia
from api.serializers.pedido import PropostaSerializer
from api.utils import methodize


def send_propostas(self, pedido, farmacias):
    """
    Metodo para envio das propostas para varias farmacias
    :param pedido: Pedido da proposta
    :param farmacias: lista dos ids das farmacias
    :return:
    """
    for farmacia in farmacias:
        # gerando json da proposta
        proposta = PropostaSerializer(instance=pedido, context={'farmacia': farmacia})
        self.send(proposta.data, id=farmacia.id)


def checkout(self, pedido, farmacia):
    """
    Metodo para envio de confirmação de checkout(Proposta aceita)
    :param pedido: Pedido da proposta
    :param farmacia: farmacia selecionada
    :return:
    """
    self.send({'pedido': {'id': pedido.id}}, id=farmacia.id)


def notifica_cancelamento(self, pedido, farmacias):
    """
    Metodo para envio de notificação de cancelamento
    :param pedido: Pedido da proposta
    :param farmacias: lista de farmacias
    :return:
    """
    for farmacia in farmacias:
        self.send({'pedido': {'id': pedido.id}}, id=farmacia.id)


class FarmaciaConsumer(BaseConsumer):
    group_name = r'farmacias-{id}'
    authenticated = True
    model = Farmacia

    def __init__(self, message=None, data=None, **kwargs):
        super(FarmaciaConsumer, self).__init__(message, data, **kwargs)
        self.send_propostas = methodize(send_propostas, self)

    def dispatch(self, *args, **kwargs):
        """
        Metodo para interpretar dados enviados do socket e direcionar o processamento
        os mesmos
        :param args:
        :param kwargs:
        :return:
        """
        print('Chegou')

    @classmethod
    def send_propostas(cls, pedido, farmacias):
        """
        Metodo para envio das propostas para varias farmacias
        :param pedido: Pedido da proposta
        :param farmacias: lista dos ids das farmacias
        """
        cls(skip_group=True).send_propostas(pedido, farmacias)

    @classmethod
    def checkout(cls, pedido, farmacia):
        """
        Metodo para envio de confirmação de checkout(Proposta aceita)
        :param pedido: Pedido da proposta
        :param farmacia: farmacia selecionada
        :return:
        """
        cls(skip_group=True).checkout(pedido, farmacia)

    @classmethod
    def notifica_cancelamento(cls, pedido, farmacias):
        """
        Metodo para envio de notificação de cancelamento
        :param pedido: Pedido da proposta
        :param farmacias: lista de farmacias
        :return:
        """
        cls(skip_group=True).notifica_cancelamento(pedido, farmacias)