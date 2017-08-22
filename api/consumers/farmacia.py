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
