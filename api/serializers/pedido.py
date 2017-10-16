import locale

from api.consumers.farmacia import FarmaciaConsumer
from api.models.enums.status_pagamento import StatusPagamento
from api.models.enums.status_pagamento_cartao import StatusPagamentoCartao
from api.models.enums.status_pedido import StatusPedido
from api.utils.generics import print_exception

from django.db import transaction
from rest_framework import serializers

from api.models.endereco import Endereco
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.enums.status_item import StatusItem
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.farmacia import Farmacia
from api.models.log import Log
from api.models.pedido import ItemPedido, Pedido, ItemPropostaPedido, PagamentoCartao
from api.serializers.apresentacao import ApresentacaoListSerializer
from api.serializers.farmacia import FarmaciaListSerializer
from api.servico_pagamento import tipo_servicos
from api.servico_pagamento.pagamento import Pagamento
from api.servico_pagamento.servicos.cielo import ServicoCielo, ResponseCieloException
from api.utils import get_client_browser, get_client_ip  # , status_transacao_cartao_cielo
from api.utils import get_user_lookup, get_tempo_proposta
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
    endereco = serializers.PrimaryKeyRelatedField(queryset=Endereco.objects.all(), required=False, write_only=True)

    class Meta:
        model = Pedido
        fields = (
            "id",
            "endereco",
            "valor_frete",
            "status",
            "log",
            "forma_pagamento",
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

    def validate(self, attrs):
        if ('delivery' not in attrs or attrs['delivery']) and ('endereco' not in attrs or attrs['endereco'] == None):
            raise serializers.ValidationError('Endereço é obrigatório quando utilizar serviço de entrega.')
        return attrs

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

            # Adicionando endereco selecionado
            endereco = validated_data.pop('endereco') if 'endereco' in validated_data else None
            if validated_data['delivery'] and endereco:
                endereco_props = (
                    "cep",
                    "uf",
                    "logradouro",
                    "numero",
                    "complemento",
                    "cidade",
                    "bairro",
                    "nome_endereco",
                    "nome_destinatario"
                )
                for prop in endereco_props:
                    validated_data[prop] = getattr(endereco, prop, None)

            # pegando o cliente da requisição
            cliente = get_user_lookup(request, 'cliente')

            validated_data['log'] = log
            validated_data['cliente'] = cliente

            # Gerando pedido
            pedido = Pedido.objects.create(**validated_data)

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
        propostas = [_ for _ in obj.propostas if _['status'] == StatusItemProposta.ENVIADO]
        for proposta in propostas:
            proposta['itens'] = ItemPropostaSimplificadoSerializer(instance=proposta['itens'], many=True).data
            proposta['farmacia'] = FarmaciaListSerializer(instance=proposta['farmacia'], context={'pedido': obj}).data

        return propostas

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
            "quantidade",
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

    def validate(self, attrs):
        itens_proposta = [item for item in self.initial_data['itens_proposta']]
        for item in itens_proposta:
            try:
                self.instance.itens_proposta.get(id=item['id'])
            except ItemPropostaPedido.DoesNotExist:
                raise serializers.ValidationError('Item não encontrado')

        if get_tempo_proposta(self.instance) == 0:
            raise serializers.ValidationError('Tempo para submeter proposta excedido.')

        return attrs

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
                _item = serializer.save()
                # Caso a quantidade seja zero coloca como não possui
                if not _item.quantidade:
                    _item.possui = False
                    _item.save()

        return super(PropostaUpdateSerializer, self).update(instance, validated_data)


class PagamentoCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoCartao
        fields = (
            "id",
            "cartao",
            "valor",
            "numero_parcelas",
            "status"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
        }

    def validate_cartao(self, data):
        if 'view' not in self.context:
            raise serializers.ValidationError('Erro de validação')
        pedido = self.context['view'].get_object()
        if data not in pedido.cliente.cartoes.all():
            raise serializers.ValidationError('Cartão não encontrado.')
        return data

    def create(self, validated_data):
        validated_data['pedido'] = self.context['view'].get_object()
        instance = super(PagamentoCartaoSerializer, self).create(validated_data)
        try:
            with transaction.atomic():
                # venda = object
                # data['venda'] = venda = VendaCartao.objects.create(
                #     motorista=data['unidade'].motorista,
                #     unidade=data['unidade'],
                #     descricao='RADIO TAXI',
                #     valor=data['valor'],
                #     bandeira=self.translate_brand(data['bandeira'])
                # )

                venda = {
                    'pedido_id': instance.pedido.id,
                    'valor': instance.valor,
                    'cvv': instance.cartao.cvv,
                    'bandeira': instance.cartao.bandeira,
                    'token': instance.cartao.token
                }

                data = Pagamento.pagar(tipo_servicos.CIELO, venda)

                json_venda, json_captura = data['venda'], data['captura']
                instance.json_venda = json_venda
                instance.json_captura = json_captura
                instance.pagamento_status = int(json_venda['Payment']['Status'])
                # venda.pagamento_numero_autorizacao = int(json_venda['Payment']['ProofOfSale']) if 'ProofOfSale' in \
                #                                                         json_venda['Payment'] else None
                pagamento_id = json_venda['Payment']['PaymentId']
                # venda.pagamento_data_recebimento = datetime.strptime(json_venda['Payment']['ReceivedDate'],
                #                                                      '%Y-%m-%d %H:%M:%S')
                # venda.pagamento_codigo_autorizacao = json_venda['Payment'][
                #     'AuthorizationCode'] if 'AuthorizationCode' in \
                #                             json_venda[
                #                                 'Payment'] else None
                # venda.pagamento_tid = str(json_venda['Payment']['Tid'])
                # venda.pagamento_mensagem_retorno = json_venda['Payment']['ReturnMessage']
                # venda.pagamento_codigo_retorno = json_venda['Payment']['ReturnCode']

                if json_captura:
                    # venda.capturado = True
                    instance.captura_status = int(json_captura['Status'])
                    # venda.captura_codigo_retorno = json_captura['ReturnCode']
                    # venda.captura_mensagem_retorno = json_captura['ReturnMessage']

                    instance.status = ServicoCielo.status_pagamento(pagamento_id)

                instance.save()

        except ResponseCieloException as err:
            print(err)
        except Exception as e:
            print(e)
            print(type(e))
            print_exception()
        return instance


class PedidoCheckoutSerializer(serializers.ModelSerializer):
    pagamentos = PagamentoCartaoSerializer(many=True, required=False)
    farmacia_selecionada = serializers.PrimaryKeyRelatedField(queryset=Farmacia.objects.all(), write_only=True)

    class Meta:
        model = Pedido
        fields = (
            "forma_pagamento",
            "pagamentos",
            "farmacia_selecionada",
            "troco"
        )

    def validate(self, attrs):
        # If para verificar se os pagamentos estão inseridos corretamente
        if (
            'forma_pagamento' not in attrs and (
                ('pagamentos' not in attrs) or ('pagamentos' in attrs and len(attrs['pagamentos']) == 0)
            )
        ) or \
            (
            'forma_pagamento' in attrs and attrs['forma_pagamento'] == FormaPagamento.CARTAO and (
                ('pagamentos' not in attrs) or ('pagamentos' in attrs and len(attrs['pagamentos']) == 0)
            )
        ):
            raise serializers.ValidationError('Em pagamentos com cartão é necessário informar pelo menos um cartão')

        # definindo a forma de pagamento
        if ('forma_pagamento' not in attrs) or \
           ('forma_pagamento' in attrs and attrs['forma_pagamento'] == FormaPagamento.CARTAO):
            attrs['forma_pagamento'] = FormaPagamento.CARTAO

            # validando se o valor esta completo, ou se esta excedendo

        else:
            attrs['forma_pagamento'] = FormaPagamento.DINHEIRO

        pedido = getattr(self, 'instance', None)

        if pedido:
            if pedido.status_pagamento == StatusPagamento.PAGO:
                raise serializers.ValidationError('Pedido ja está pago.')
            elif pedido.status_pagamento == StatusPagamento.CANCELADO:
                raise serializers.ValidationError('Status de pagamento está cancelado.')

            if attrs['forma_pagamento'] == FormaPagamento.CARTAO:
                pagamentos = attrs['pagamentos']
                valor_pedido = pedido.get_total_farmacia(attrs['farmacia_selecionada'])
                total_a_pagar = sum(_['valor'] for _ in pagamentos)

                if pedido.pagamentos.filter(status=StatusPagamentoCartao.PAGAMENTO_CONFIRMADO).count():
                    pagamentos = pedido.pagamentos.filter(status=StatusPagamentoCartao.PAGAMENTO_CONFIRMADO)
                    total_pago = sum(p.valor for p in pagamentos)
                    divida = valor_pedido - total_pago
                    if total_a_pagar > divida:
                        raise serializers.ValidationError('Total pago superior ao resto do pedido.')

                    if total_a_pagar < divida:
                        raise serializers.ValidationError('Total pago inferior ao resto do pedido.')
                else:
                    if total_a_pagar > valor_pedido:
                        raise serializers.ValidationError('Total pago superior ao valor do pedido.')

                    if total_a_pagar < valor_pedido:
                        raise serializers.ValidationError('Total pago inferior ao valor do pedido.')

        else:
            raise serializers.ValidationError('Deve haver pedido no checkout.')

        return attrs

    def validate_farmacia_selecionada(self, data):
        if not self.instance.farmacia_esta_nas_propostas(data):
            raise serializers.ValidationError('Farmacia não realizou proposta para este pedido.')
        return data

    def update(self, instance, validated_data):

        if validated_data['forma_pagamento'] == FormaPagamento.CARTAO:
            pagamentos = validated_data.pop('pagamentos')
            for item in pagamentos:
                item['cartao'] = item['cartao'].id
                serializer = PagamentoCartaoSerializer(data=item, context=self.context)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        farmacia = validated_data.pop('farmacia_selecionada')
        instance.itens.update(farmacia=farmacia)
        proposta = [_ for _ in instance.propostas if _['farmacia'].id == farmacia.id][0]
        itens_proposta = proposta['itens']
        instance.status = StatusPedido.ACEITO
        instance.save()
        for item in instance.itens.all():
            item_proposta = itens_proposta.get(apresentacao=item.apresentacao)
            item.valor_unitario = item_proposta.valor_unitario
            item.quantidade_atendida = item_proposta.quantidade
            item.status = StatusItem.ABERTO if item_proposta.possui else StatusItem.CANCELADO
            item.save()

        instance = super(PedidoCheckoutSerializer, self).update(instance, validated_data)
        if instance.forma_pagamento == FormaPagamento.DINHEIRO:
            instance.status_pagamento = StatusPagamento.PAGO
            instance.save()
            FarmaciaConsumer.checkout(instance, farmacia)
        else:
            if instance.pagamentos.filter(status=StatusPagamentoCartao.PAGAMENTO_CONFIRMADO).count():
                pagamentos = instance.pagamentos.filter(status=StatusPagamentoCartao.PAGAMENTO_CONFIRMADO)
                total_pago = sum(p.valor for p in pagamentos)
                total = sum(
                    item.valor_unitario * item.quantidade_atendida
                    for item in instance.itens.filter(status=StatusItem.ENVIADO)
                )
                if total == total_pago:
                    instance.status_pagamento = StatusPagamento.PAGO
                    instance.save()
                    FarmaciaConsumer.checkout(instance, farmacia)
        return instance
