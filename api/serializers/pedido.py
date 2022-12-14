import locale

from django.db import transaction
from datetime import datetime, timedelta
from rest_framework import serializers

from api.models.log import Log
from api.models.endereco import Endereco
from api.models.farmacia import Farmacia

from api.models.ultimo_preco import UltimoPreco
from api.models.conta_pagar import ContaPagar
from api.models.configuracao import Configuracao
from api.models.conta_receber import ContaReceber
from api.models.administradora import Administradora
from api.models.representante_legal import RepresentanteLegal
from api.models.pedido import ItemPedido, Pedido, ItemPropostaPedido, LogData
from api.models.notificacao import Notificacao, NotificacoesTemplate, TipoNotificacaoTemplate

from api.models.enums import PagadorContas
from api.models.enums.tipo_venda import TipoVenda
from api.models.enums.status_item import StatusItem
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.enums.status_pagamento import StatusPagamento
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.enums.status_pagamento_cartao import StatusPagamentoCartao
from api.models.enums.status_pedido import StatusPedido

from api.utils.generics import print_exception
from api.utils.firebase_utils import enviar_notif
from api.utils.usuario_teste import check_user_eh_teste, fazer_proposta_faker

from api.serializers.cartao import CartaoSerializer
from api.serializers.apresentacao import ApresentacaoListSerializer
from api.serializers.farmacia import FarmaciaListSerializer, FarmaciaEnderecoSerializer, FarmaciaComandaDado

from api.servico_pagamento import tipo_servicos
from api.servico_pagamento.pagamento import Pagamento
from api.servico_pagamento.servicos.cielo import ServicoCielo, ResponseCieloException

from api.utils import get_client_browser, get_client_ip  # , status_transacao_cartao_cielo
from api.utils import get_user_lookup, get_tempo_proposta

from api.serializers.log import LogSerializer

from api.consumers.farmacia import FarmaciaConsumer

from apiv2.serializers.apresentacao import ApresentacaoPropostaItemSerializer

class PagamentoCartao(object):
    pass


class LogDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = (
            'mes',
            'ano'
        )


class AnnotationPedidoSerializer(serializers.Serializer):
    data_criacao = serializers.DateTimeField()
    valor_bruto = serializers.CharField()
    valor_liquido = serializers.CharField()


class PedidoMinimalSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()
    data_criacao = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = (
            "id",
            "status",
            "forma_pagamento",
            "delivery",
            "valor_liquido",
            "data_atualizacao",
            "data_criacao",
            "cliente",
            "valor_frete",
            "valor_comissao_administradora",
            "valor_comissao_thefarma",
            "valor_bruto"
        )

    def get_data_atualizacao(self, obj):
        return obj.log.data_atualizacao

    def get_data_criacao(self, obj):
        return obj.log.data_criacao
    
    def get_cliente(self, obj):
        return str(obj.cliente)


class PedidoTotaisSerializer(serializers.Serializer):
    liquido = serializers.CharField()
    bruto = serializers.CharField()


class ItemPedidoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPedido
        fields = (
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "status"
        )
        extra_kwargs = {
            'valor_unitario': {'read_only': True},
            'status': {'read_only': True},
        }


class ItemPedidoSerializer(serializers.ModelSerializer):
    apresentacao = ApresentacaoListSerializer(read_only=True)
    quantidade = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = (
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "status"
        )
        extra_kwargs = {
            'quantidade': {'read_only': True},
            'apresentacao': {'read_only': True},
            'valor_unitario': {'read_only': True},
            'status': {'read_only': True},
        }
    
    def get_quantidade(self,obj):
        if obj.pedido.status == StatusPedido.ABERTO:
            return obj.quantidade
        else:
            return obj.quantidade_atendida

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
            "itens",
            "uf"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'valor_frete': {'read_only': True},
        }

    def validate(self, attrs):
        if ('delivery' not in attrs or attrs['delivery']) and ('endereco' not in attrs or attrs['endereco'] == None):
            raise serializers.ValidationError('Endere??o ?? obrigat??rio quando utilizar servi??o de entrega.')
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            # request passada no contexto do serializer
            request = self.context['request']

            # removendo os itens do validated_data
            itens = validated_data.pop('itens')

            # gerando log do pedido com o agent e o ip da requisi????o
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
                    if prop == 'uf':
                        if 'uf' not in validated_data:
                            validated_data[prop] = getattr(endereco, prop, None)
                        if ('uf' in validated_data and validated_data['uf'] == '') or ('uf' in validated_data and validated_data['uf'] is None):
                            validated_data[prop] = getattr(endereco, prop, None)
                    else:
                        validated_data[prop] = getattr(endereco, prop, None)

            # pegando o cliente da requisi????o
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
                apresentacao.get_manager.update_ranking_proposta(apresentacao.id)
                # Buscando o pmc base para calcular o valor unit??rio
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
    farmacia = serializers.SerializerMethodField()
    bairro = serializers.SerializerMethodField()
    cartao = CartaoSerializer()
    data_criacao = serializers.SerializerMethodField()

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
            "farmacia",
            "cartao",
            "status_pagamento",
            "status_cartao",
            "valor_bruto",
            "valor_liquido",
            "numero_parcelas",
            "itens",
            "data_criacao"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'valor_frete': {'read_only': True},
        }

    def get_bairro(self, obj):
        if obj.bairro:
            return obj.bairro
        return ''

    def get_farmacia(self, obj):
        if obj.farmacia:
            serializer = FarmaciaEnderecoSerializer(instance=obj.farmacia, context={'pedido': obj})
            return serializer.data
        return None

    def get_data_criacao(self, obj):
        if obj.log:
            return (obj.log.data_criacao.timestamp() * 1000)
        return None


class ItemPropostaSimplificadoSerializer(serializers.ModelSerializer):
    apresentacao = ApresentacaoPropostaItemSerializer(read_only=True)
    #apresentacao_pedida = ApresentacaoPropostaItemSerializer(read_only=True)
    produto_pesquisado =  serializers.SerializerMethodField()

    class Meta:
        model = ItemPropostaPedido
        fields = (
            "produto_pesquisado",
            "apresentacao",
            "quantidade",
            "valor_unitario",
            "possui",
            "quantidade_inferior",
            "permutacao_id",
        )
        extra_kwargs = {
            "quantidade": {'read_only': True},
            'apresentacao': {'read_only': True},
            'valor_unitario': {'read_only': True},
            'possui': {'read_only': True},
            'quantidade_inferior': {'read_only': True},
        }

    def get_produto_pesquisado(self, obj):
        try:
            return obj.produto_pesquisado.nome
        except Exception as error:
            return obj.apresentacao.produto.nome


class PedidoDetalhadoSerializer(PedidoSerializer):
    propostas = serializers.SerializerMethodField()
    farmacia = serializers.SerializerMethodField()
    bairro = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    cartao = CartaoSerializer()

    def get_propostas(self, obj):
        propostas = [_ for _ in obj.propostas if _['status'] == StatusItemProposta.ENVIADO]
        for proposta in propostas:
            proposta['itens'] = ItemPropostaSimplificadoSerializer(instance=proposta['itens'], many=True).data
            proposta['farmacia'] = FarmaciaEnderecoSerializer(instance=proposta['farmacia'], context={'pedido': obj}).data

        return propostas

    class Meta:
        model = Pedido
        fields = (
            "id",
            "data_criacao",
            "valor_frete",
            "status",
            "views",
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
            "farmacia",
            "cartao",
            "status_pagamento",
            "status_cartao",
            "valor_bruto",
            "valor_liquido",
            "numero_parcelas",
            "itens",
            "propostas",
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'log': {'read_only': True},
            'status': {'read_only': True},
            'valor_frete': {'read_only': True},
        }

    def get_views(self, obj):
        if obj.views:
            return obj.views
        return 0

    def get_bairro(self, obj):
        if obj.bairro:
            return obj.bairro
        return ''

    def get_farmacia(self, obj):
        if obj.farmacia:
            serializer = FarmaciaEnderecoSerializer(instance=obj.farmacia, context={'pedido': obj})
            return serializer.data
        return None


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
            "possui",
            "quantidade_inferior",
            "tipo_venda",
            "permutacao_id"
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'quantidade': {'read_only': True},
            'apresentacao': {'read_only': True},
            'status': {'read_only': True},
            'farmacia': {'read_only': True},
            'quantidade_inferior': {'read_only': True},
        }


class PropostaSerializer(serializers.ModelSerializer):
    tempo = serializers.SerializerMethodField(read_only=True)
    cliente = serializers.CharField(read_only=True, source='cliente.usuario.get_full_name')
    itens_proposta = serializers.SerializerMethodField(read_only=True)
    bairro = serializers.SerializerMethodField(read_only=True)
    log = LogSerializer(read_only=True)
    status_submissao = serializers.SerializerMethodField()

    def get_permutacao_id(self, obj):
        if 'farmacia' in self.context:
            obj.itens_proposta.filter(farmacia=self.context['farmacia']).first().permutacao_id
        return None
    
    def get_bairro(self, obj):
        if obj.bairro:
            return obj.bairro
        return ''

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
        return StatusItemProposta.ABERTO.value

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


class ItemPropostaUpdateSerializer(serializers.ModelSerializer):
    possui = serializers.NullBooleanField(required=False)
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
        #verifica se ao menos um item tem quantidade
        # if not any(map(lambda x : x['quantidade'],itens_proposta)):
        #     raise serializers.ValidationError('Ao menos um item deve ter quantidade valida!')
        # #verifica se possui ao menos um item
        # if not any(map(lambda x : x['possui'],itens_proposta)):
        #     raise serializers.ValidationError('Voce deve possuir ao menos um item!')
        for item in itens_proposta:
            try:
                self.instance.itens_proposta.get(id=item['id'])
            except ItemPropostaPedido.DoesNotExist:
                raise serializers.ValidationError('Item n??o encontrado')

        if get_tempo_proposta(self.instance) == 0:
            raise serializers.ValidationError('Tempo para submeter proposta excedido.')
        
        return attrs

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        validated_data.pop('itens_proposta')
        itens_proposta = [item for item in self.initial_data['itens_proposta']]
        #verifica se ao menos uma quantidade acima de 0
        if any(map(lambda x : x['quantidade'], itens_proposta)):
            for item in itens_proposta:
                #ignora o possui que veio
                item.pop('possui', None)
                #verifica a quantidade e atribui o valor do possui
                item['possui'] = True if item['quantidade'] > 0 else False
                #recupera a instancia no banco e diz que foi enviado
                item_proposta = instance.itens_proposta.get(id=item['id'])
                item_proposta.status = StatusItemProposta.ENVIADO
                serializer = ItemPropostaUpdateSerializer(instance=item_proposta, data=item)
                if serializer.is_valid():
                    _item = serializer.save()
                    self.atualiza_preco_farmacia(_item)
            #envia a notificacao pro app
            #verifica se ele ja foi notificado pela farmacia atual
            farmacia = self.context['request'].user.representante_farmacia.farmacia
            total_notifcacao = Notificacao.objects.filter(
                pedido=instance,
                template__tipo=TipoNotificacaoTemplate.NOVA_PROPOSTA,
                farmacia=farmacia
            )
            if (not total_notifcacao.count()):
                enviar_notif(instance.cliente.fcm_token,TipoNotificacaoTemplate.NOVA_PROPOSTA,instance.cliente.id,instance,extra_data={'pedido_id':instance.id},farmacia=farmacia)
                
        #pusher notification
        # instance.status = StatusPedido.ACEITO
        # instance.save()
        
        #manda mensagem no WS
        farmacia = RepresentanteLegal.objects.get(usuario=self.context['request'].user).farmacia
        FarmaciaConsumer.fechar_cards_proposta(instance,farmacia)
        return super(PropostaUpdateSerializer, self).update(instance, validated_data)

    def atualiza_preco_farmacia(self,item):
        """
        Atualiza o ulitmo preco que a farmacia ofereceu no produto, caso nao tenha eh criado
        """
        ultimo_preco, created = UltimoPreco.objects.get_or_create(farmacia_id=item.farmacia.id,apresentacao_id=item.apresentacao.id)
        ultimo_preco.valor = item.valor_unitario
        ultimo_preco.save()




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
            raise serializers.ValidationError('Erro de valida????o')
        pedido = self.context['view'].get_object()
        if data not in pedido.cliente.cartoes.all():
            raise serializers.ValidationError('Cart??o n??o encontrado.')
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
    permutacao_id = serializers.IntegerField()
    class Meta:
        model = Pedido
        fields = (
            "forma_pagamento",
            "farmacia",
            "troco",
            "cartao",
            "numero_parcelas",
            "permutacao_id",
        )

    def validate_farmacia(self, data):
        if not self.instance.farmacia_esta_nas_propostas(data):
            raise serializers.ValidationError('Farmacia n??o realizou proposta para este pedido.')
        return data

    def validate_cartao(self, data):
        if data:
            if 'view' not in self.context:
                raise serializers.ValidationError('Erro de valida????o')
            pedido = self.context['view'].get_object()
            if data not in pedido.cliente.cartoes.all():
                raise serializers.ValidationError('Cart??o n??o encontrado.')
        return data

    def validate(self, attrs):
        # If para verificar se os pagamentos est??o inseridos corretamente
        if 'forma_pagamento' not in attrs or (
                'forma_pagamento' in attrs and attrs['forma_pagamento'] == FormaPagamento.CARTAO) and (
                ('cartao' not in attrs) or ('cartao' in attrs and not attrs['cartao'])):
            raise serializers.ValidationError('Em pagamentos com cart??o ?? necess??rio informar pelo menos um cart??o')

        # definindo a forma de pagamento
        if ('forma_pagamento' not in attrs) or \
           ('forma_pagamento' in attrs and attrs['forma_pagamento'] == FormaPagamento.CARTAO):
            attrs['forma_pagamento'] = FormaPagamento.CARTAO

        else:
            attrs['forma_pagamento'] = FormaPagamento.DINHEIRO

        if 'permutacao_id' not in attrs:
            raise serializers.ValidationError('Informe a proposta escolhida.')

        pedido = getattr(self, 'instance', None)

        if pedido:
            if pedido.status_pagamento == StatusPagamento.PAGO:
                raise serializers.ValidationError('Pedido j?? est?? pago.')
            elif pedido.status_pagamento == StatusPagamento.CANCELADO:
                raise serializers.ValidationError('Status de pagamento est?? cancelado.')
        else:
            raise serializers.ValidationError('Deve haver pedido no checkout.')

        return attrs

    def notifcar_cliente(self,pedido):
        """
        Metodo que faz a notificacao para um cliente
        """
        tipo = None
        medicamento_receita = False
        if pedido.itens.filter(apresentacao__produto__principio_ativo__tipo_venda=TipoVenda.COM_RECEITA).count():
            medicamento_receita = True

        if(not pedido.delivery):
            if(medicamento_receita):
                #medicamento com receita
                if(pedido.forma_pagamento == FormaPagamento.DINHEIRO):
                    tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_DINHEIRO_COM_RECEITA
                else:
                    tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_CARTAO_COM_RECEITA
            else:
                #medicamento sem receita
                if(pedido.forma_pagamento == FormaPagamento.CARTAO):
                    tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_CARTAO_NORM
                else:
                    tipo = TipoNotificacaoTemplate.B_AGUARDANDO_EM_DINHEIRO_NORM
                    
            enviar_notif(pedido.cliente.fcm_token,tipo,pedido.cliente.id,pedido,extra_data={'pedido_id':pedido.id})

    def update(self, instance, validated_data):
        with transaction.atomic():
            #limpa as propostas n??o selecionadas
            farmacia = validated_data['farmacia']
            permutacao_id = validated_data['permutacao_id']
            instance.clear_proposal(farmacia.id, permutacao_id)

            instance = self.valida_pagamento(instance, validated_data)
            self.gerar_contas(instance)
            #notifica o cliente
            self.notifcar_cliente(instance)
        return instance

    def gerar_contas(self, pedido):
        comissao_parcela, diff = pedido.comissao

        if pedido.forma_pagamento == FormaPagamento.CARTAO:
            percentual_administradora_cartao = 0
            percentual_administradora_thefarma = 0
            valor_parcela = 0

            # calculando valor da parcela quando a venda ?? a cart??o
            if pedido.administradora_cartao:
                valor_parcela = (pedido.valor_bruto / pedido.numero_parcelas)

            if pedido.administradora_cartao and pedido.numero_parcelas == 1:
                # credido a vista
                percentual_administradora_cartao = pedido.administradora_cartao.percentual_credito_avista_farmacia
                percentual_administradora_thefarma = pedido.administradora_cartao.percentual_credito_avista_thefarma
            elif pedido.administradora_cartao and pedido.numero_parcelas > 1:
                # credito parcelado
                percentual_administradora_cartao = pedido.administradora_cartao.percentual_credito_parcelado_farmacia
                percentual_administradora_thefarma = pedido.administradora_cartao.percentual_credito_parcelado_thefarma

            dia_vencimento_conta_receber = datetime.now().date() + timedelta(pedido.administradora_cartao.dias_recebimento + 1)

            for parcela in range(1, pedido.numero_parcelas + 1):
                conta_receber = ContaReceber.objects.create(
                    numero_parcela=parcela,
                    valor_parcela=valor_parcela, # Valor bruto da parcela
                    pedido=pedido,
                    pagador=PagadorContas.ADMINISTRADORA,
                    data_vencimento=dia_vencimento_conta_receber,
                    percentual_administradora_cartao=percentual_administradora_cartao,
                    percentual_administradora_thefarma=percentual_administradora_thefarma,
                    valor_comissao=comissao_parcela if parcela > 1 else float(comissao_parcela) + float(diff)
                )

                if parcela == 1:
                    pedido.valor_comissao_thefarma = (float(comissao_parcela) + float(diff))
                    pedido.valor_comissao_administradora = conta_receber.valor_administradora_cartao
                    pedido.valor_liquido = (
                        float(pedido.valor_bruto) -
                        float(pedido.valor_comissao_thefarma) -
                        float(pedido.valor_comissao_administradora) -
                        float(pedido.valor_frete)
                    )

                    pedido.save()

            self.instance = pedido

        elif pedido.forma_pagamento == FormaPagamento.DINHEIRO:
            pedido.valor_comissao_thefarma = (float(comissao_parcela) + float(diff))
            pedido.valor_liquido = (
                float(pedido.valor_bruto) - 
                float(pedido.valor_comissao_thefarma) -
                float(pedido.valor_frete)
            )
            pedido.save()


    def valida_pagamento(self, instance, validated_data):
        farmacia = validated_data['farmacia']
        permutacao_id = validated_data['permutacao_id']

        valor_total = instance.get_total_farmacia(farmacia)
        valor_frete = farmacia.valor_frete

        validated_data['valor_bruto_sem_frete'] = valor_total

        if instance.delivery:
            validated_data['valor_frete'] = valor_frete
            valor_total = valor_total + valor_frete

        validated_data['valor_bruto'] = valor_total

        #verifica se eh o usuario teste
        if not check_user_eh_teste(self.context['request'].user):
            if validated_data['forma_pagamento'] == FormaPagamento.CARTAO:
                cartao = validated_data['cartao']
                try:
                    venda = {
                        'pedido_id': instance.id,
                        'valor': valor_total,
                        'cvv': cartao.cvv,
                        'bandeira': cartao.bandeira,
                        'token': cartao.token
                    }

                    data = Pagamento.pagar(tipo_servicos.CIELO, venda)

                    json_venda, json_captura = data['venda'], data['captura']
                    instance.json_venda = json_venda
                    instance.json_captura = json_captura
                    instance.pagamento_status = int(json_venda['Payment']['Status'])
                    pagamento_id = json_venda['Payment']['PaymentId']

                    if json_captura:
                        instance.captura_status = int(json_captura['Status'])
                        instance.status_cartao = ServicoCielo.status_pagamento(pagamento_id)

                    instance.save()
                except ResponseCieloException as err:
                    print(err)
                except Exception as e:
                    print(e)
                    print(type(e))
                    print_exception()
            else:
                #confirma o pagamento automaticamente
                instance.status_cartao = StatusPagamentoCartao.PAGAMENTO_CONFIRMADO

            if instance.status_cartao != StatusPagamentoCartao.PAGAMENTO_CONFIRMADO:
                raise serializers.ValidationError({'non_field_errors': 'Pagamento n??o confirmado'})
        
        proposta = [_ for _ in instance.propostas if _['farmacia'].id == farmacia.id][0]
        itens_proposta = proposta['itens']

        for item in instance.itens.all():
            item_proposta = itens_proposta.get(apresentacao_pedida=item.apresentacao)
            item.apresentacao = item_proposta.apresentacao
            item.valor_unitario = item_proposta.valor_unitario
            item.quantidade_atendida = item_proposta.quantidade
            if item_proposta.possui:
                item.status = StatusItem.CONFIRMADO
                item.percentual_similar = farmacia.percentual_similar
                item.percentual_etico = farmacia.percentual_etico
                item.percentual_generico = farmacia.percentual_generico
                item.percentual_nao_medicamentos = farmacia.percentual_nao_medicamentos
                item.apresentacao.get_manager.update_ranking_compra(item.apresentacao.id)
            else:
                item.status = StatusItem.CANCELADO

            item.save()

        instance = super(PedidoCheckoutSerializer, self).update(instance, validated_data)

        if instance.forma_pagamento == FormaPagamento.DINHEIRO:
            instance.status_pagamento = StatusPagamento.PAGO
            if instance.delivery:
                instance.status = StatusPedido.AGUARDANDO_ENVIO_FARMACIA
            else:
                instance.status = StatusPedido.AGUARDANDO_RETIRADA_CLIENTE

            instance.save()
            FarmaciaConsumer.checkout(instance, farmacia)
        elif instance.status_cartao == StatusPagamentoCartao.PAGAMENTO_CONFIRMADO:
            instance.status_pagamento = StatusPagamento.PAGO
            instance.administradora_cartao = Administradora.objects.first()
            if instance.delivery:
                instance.status = StatusPedido.AGUARDANDO_ENVIO_FARMACIA
            else:
                instance.status = StatusPedido.AGUARDANDO_RETIRADA_CLIENTE

            instance.save()
            FarmaciaConsumer.checkout(instance, farmacia)

        return instance


class VendaPedido(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ('pedido','data','quantidade','total_liquido')
    
    def get_data(self,obj):
        return obj.pedido.data_criacao.strftime('%d %b %Y %H:%M')
    
    def to_representation(self,instance):
        """
        formata a saida
        """
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        ret = super().to_representation(instance)
        ret['total_liquido'] = locale.currency(ret['total_liquido'])
        return ret


class ComandaPedidoSerializer(serializers.ModelSerializer):

    cliente_nome = serializers.SerializerMethodField()
    telefone = serializers.SerializerMethodField()
    valor_pago = serializers.SerializerMethodField()
    valor_troco = serializers.SerializerMethodField()
    farmacia = serializers.SerializerMethodField()
    itens_pedido = serializers.SerializerMethodField()
    forma_pagamento = serializers.SerializerMethodField()
    data_criacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = (
            'id',
            'cliente_nome',
            'telefone',
            'cep',
            'bairro',
            'numero',
            'logradouro',
            'complemento',
            'valor_pago',
            'valor_troco',
            'cidade',
            'farmacia',
            'itens_pedido',
            'forma_pagamento',
            'id',
            'data_criacao'
        )
    
    def get_cliente_nome(self,obj):
        return '{} {}'.format(obj.cliente.usuario.first_name,obj.cliente.usuario.last_name) 
    
    def get_telefone(self,obj):
        return obj.cliente.celular_formatado
    
    def get_valor_troco(self,obj):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(obj.troco, grouping=True)
    
    def get_valor_pago(self,obj):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(obj.valor_bruto, grouping=True)
    
    def get_farmacia(self,obj):
        try:
            serializer = FarmaciaComandaDado(instance=obj.farmacia)
            return serializer.data
        except Exception as e:
            print(str(e))
            return {}
    
    def get_itens_pedido(self,obj):
        rs = []
        for item in obj.itens.all():
            rs.append({
                'linha':item.apresentacao.produto.nome,
                'quantidade':item.quantidade_atendida
            })
        return rs
    
    def get_forma_pagamento(self,obj):
        if obj.forma_pagamento == FormaPagamento.CARTAO:
            return 'Cartao'
        elif obj.forma_pagamento == FormaPagamento.DINHEIRO:
            return 'Dinheiro'
    
    def get_data_criacao(self,obj):
        return obj.data_criacao.strftime('%d/%m/%Y')