import locale

from rest_framework import serializers
from django.db import transaction

from api.models.pedido import Pedido, ItemPedido
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


class ItemPedidoSerializer(serializers.ModelSerializer):

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


class PedidoSerializer(serializers.ModelSerializer):
    log = LogSerializer()
    itens = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = (
            "valor_frete",
            "numero_parcelas",
            "status",
            "log",
            "forma_pagamento",
            "cep",
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
            itens = validated_data.pop('itens')
            pedido = Pedido.objects.create(**validated_data)
            for item_data in itens:
                ItemPedido.objects.pedido(pedido=pedido, **item_data)
            return pedido
