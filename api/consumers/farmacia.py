from rest_framework import serializers
from api.mixins.consumers import BaseConsumer
from api.models.farmacia import Farmacia
from api.models.pedido import Pedido, ItemPropostaPedido
from api.serializers.apresentacao import ApresentacaoListSerializer
from api.serializers.log import LogSerializer
from api.utils import methodize
from api.utils.generics import get_tempo_proposta


class ItemPropostaSerializer(serializers.ModelSerializer):
    apresentacao = serializers.SerializerMethodField()

    def get_apresentacao(self, obj):
        return ApresentacaoListSerializer(read_only=True, instance=obj.apresentacao, context=self.context).data

    class Meta:
        model = ItemPropostaPedido
        fields = (
            "id",
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "farmacia",
            "status",
            "possui"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'quantidade': {'read_only': True},
            'apresentacao': {'read_only': True},
            'status': {'read_only': True},
            'farmacia': {'read_only': True},
        }


class PropostaSerializer(serializers.ModelSerializer):
    tempo = serializers.SerializerMethodField(read_only=True)
    cliente = serializers.CharField(read_only=True, source='cliente.usuario.get_full_name')
    itens_proposta = serializers.SerializerMethodField(read_only=True)
    log = LogSerializer(read_only=True)
    status_submissao = serializers.SerializerMethodField()

    def get_tempo(self, obj):
        return get_tempo_proposta(obj)

    def get_itens_proposta(self, obj):
        if 'farmacia' in self.context:
            context = {
                'cidade': self.context['farmacia'].endereco.cidade,
            }
            itens_proposta = ItemPropostaSerializer(
                many=True,
                instance=obj.itens_proposta.filter(farmacia=self.context['farmacia']),
                context=context
            )
            return itens_proposta.data
        return []

    def get_status_submissao(self, obj):
        if 'farmacia' in self.context:
            farmacia = self.context['farmacia']
            return farmacia.get_status_proposta(obj).value
        return 0

    class Meta:
        model = Pedido
        fields = (
            "id",
            "valor_frete",
            "status",
            "log",
            "forma_pagamento",
            "cep",
            "uf",
            "logradouro",
            "numero",
            "complemento",
            "cidade",
            "bairro",
            "nome_endereco",
            "nome_destinatario",
            "delivery",
            "troco",
            "itens_proposta",
            "cliente",
            "tempo",
            "farmacia",
            "status_submissao"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'forma_pagamento': {'read_only': True},
            'cep': {'read_only': True},
            'uf': {'read_only': True},
            'logradouro': {'read_only': True},
            'cidade': {'read_only': True},
            'bairro': {'read_only': True},
            'nome_endereco': {'read_only': True},
            'nome_destinatario': {'read_only': True},
            'numero': {'read_only': True},
            'delivery': {'read_only': True},
            'troco': {'read_only': True},
        }


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
    # Tipo 1 checkout
    proposta = PropostaSerializer(instance=pedido, context={'farmacia': farmacia})
    self.send({'pedido': proposta.data, 'tipo': 1}, id=farmacia.id)


def notifica_cancelamento(self, pedido, farmacias):
    """
    Metodo para envio de notificação de cancelamento
    :param pedido: Pedido da proposta
    :param farmacias: lista de farmacias
    :return:
    """
    # Tipo 0 cancelamento
    for farmacia in farmacias:
        proposta = PropostaSerializer(instance=pedido, context={'farmacia': farmacia})
        self.send({'pedido': proposta.data, 'tipo': 0}, id=farmacia.id)


class FarmaciaConsumer(BaseConsumer):
    group_name = r'farmacias-{id}'
    authenticated = True
    model = Farmacia

    def __init__(self, message=None, data=None, **kwargs):
        super(FarmaciaConsumer, self).__init__(message, data, **kwargs)
        self.send_propostas = methodize(send_propostas, self)
        self.checkout = methodize(checkout, self)
        self.notifica_cancelamento = methodize(notifica_cancelamento, self)

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
