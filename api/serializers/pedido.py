import locale

from django.db import models
from django.db import transaction
from rest_framework import serializers

from api.models.configuracao import Configuracao
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.log import Log
from api.models.pedido import ItemPedido, Pedido, ItemPropostaPedido
from api.serializers.apresentacao import ApresentacaoListSerializer
from api.serializers.farmacia import FarmaciaListSerializer
from api.utils import get_client_browser, get_client_ip
from api.utils.generics import get_user_lookup
from datetime import datetime, timedelta
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


class ItemPropostaSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPropostaPedido
        fields = (
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "possui"
        )
        extra_kwargs = {
            "quantidade": {'read_only': True},
            'apresentacao': {'read_only': True},
            'valor_unitario': {'read_only': True},
            'possui': {'read_only': True},
        }


class PedidoDetalhadoSerializer(PedidoSerializer):
    propostas = serializers.SerializerMethodField()

    def get_propostas(self, obj):
        propostas = obj.propostas
        for proposta in propostas:
            proposta['itens'] = ItemPropostaSimplificadoSerializer(instance=proposta['itens'], many=True).data
            proposta['farmacia'] = FarmaciaListSerializer(instance=proposta['farmacia']).data

        return propostas

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
            "itens",
            "propostas"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'valor_frete': {'read_only': True},
        }


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

    def get_tempo(self, obj):
        try:
            duracao_proposta = Configuracao.objects.first().duracao_proposta
        except:
            duracao_proposta = timedelta(minutes=5)
        return (duracao_proposta - (datetime.now() - obj.log.data_criacao)).total_seconds()

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
            "tempo"
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


class ItemPropostaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPropostaPedido
        fields = (
            "id",
            "valor_unitario",
            "possui"
        )
        extra_kwargs = {'id': {'read_only': True}, }


class PropostaUpdateSerializer(serializers.ModelSerializer):
    itens_proposta = ItemPropostaUpdateSerializer(many=True)

    class Meta:
        model = Pedido
        fields = (
            "id",
            "itens_proposta"
        )
        extra_kwargs = {'id': {'read_only': True}, }

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        validated_data.pop('itens_proposta')

        itens_proposta = [item for item in self.initial_data['itens_proposta']]

        for item in itens_proposta:
            item_proposta = instance.itens_proposta.get(id=item['id'])
            item_proposta.status = StatusItemProposta.ENVIADO
            serializer = ItemPropostaUpdateSerializer(instance=item_proposta, data=item)
            if serializer.is_valid():
                serializer.save()

        return super(PropostaUpdateSerializer, self).update(instance, validated_data)