import locale

from django.db import transaction
from rest_framework import serializers

from api.models.log import Log
from api.models.pedido import ItemPedido, Pedido
from api.serializers.apresentacao import ApresentacaoListSerializer
from api.utils import get_client_browser, get_client_ip
from api.utils.generics import get_user_lookup

from .log import LogSerializer

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class PedidoSimplesSerializer(serializers.ModelSerializer):
    data_criacao = serializers.DateTimeField(read_only=True, source='log.data_criacao')
    valor_bruto = serializers.SerializerMethodField()
    valor_liquido = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ('id', 'data_criacao', 'valor_bruto', 'valor_liquido', 'status')

    def get_valor_bruto(self, obj):
        return locale.currency(obj.valor_bruto, grouping=True, symbol=None)

    def get_valor_liquido(self, obj):
        return locale.currency(obj.valor_liquido, grouping=True, symbol=None)


class ItemPedidoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPedido
        fields = (
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "farmacia",
            "status"
        )
        extra_kwargs = {
            'valor_unitario': {'read_only': True},
            'status': {'read_only': True},
            'farmacia': {'read_only': True},
        }


class ItemPedidoSerializer(serializers.ModelSerializer):
    apresentacao = ApresentacaoListSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = (
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "farmacia",
            "status"
        )
        extra_kwargs = {
            'quantidade': {'read_only': True},
            'apresentacao': {'read_only': True},
            'valor_unitario': {'read_only': True},
            'status': {'read_only': True},
            'farmacia': {'read_only': True},
        }


class PedidoCreateSerializer(serializers.ModelSerializer):
    log = LogSerializer(read_only=True)
    itens = ItemPedidoCreateSerializer(many=True)

    class Meta:
        model = Pedido
        fields = (
            "id",
            "valor_frete",
            "numero_parcelas",
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
            "latitude",
            "longitude",
            "delivery",
            "troco",
            "itens"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'valor_frete': {'read_only': True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            # request passada no contexto do serializer
            request = self.context['request']

            # removendo os itens do validated_data
            itens = validated_data.pop('itens')

            # gerando log do pedido com o agent e o ip da requisição
            log = Log.objects.create(
                browser=get_client_browser(request),
                remote_ip=get_client_ip(request)
            )

            # pegando o cliente da requisição
            cliente = get_user_lookup(request, 'cliente')

            # Gerando pedido
            pedido = Pedido.objects.create(**validated_data, log=log, cliente=cliente)

            cidade = pedido.cidade_obj

            # Salvando os itens do pedido
            for item_data in itens:
                valor_unitario = 0
                apresentacao = item_data["apresentacao"]

                # Buscando o pmc base para calcular o valor unitário
                try:
                    tabela = apresentacao.tabelas.get(icms=cidade.uf.icms)
                    valor_unitario = tabela.pmc
                except Exception as err:
                    print(err)

                item_data['pedido'] = pedido
                item_data['valor_unitario'] = valor_unitario
                ItemPedido.objects.create(**item_data)

            return pedido


class PedidoSerializer(PedidoCreateSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
