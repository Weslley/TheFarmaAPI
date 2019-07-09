from rest_framework import serializers
from api.models.pedido import Pedido
from api.models.endereco import Endereco
from api.serializers.log import LogSerializer
from django.db import transaction
from api.models.apresentacao import Apresentacao
from apiv2.utils.custom_fields import ListPrimaryKeyRelatoionField
from api.utils import get_client_browser, get_client_ip 
from api.models.log import Log
from api.utils import get_user_lookup, get_tempo_proposta



class ItemPedidoCreateSerializer(serializers.Serializer):
    apresentacao = ListPrimaryKeyRelatoionField(queryset=Apresentacao.objects.all())
    quantidade = serializers.IntegerField()

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
    
    def create(self,validated_data):
        with transaction.atomic():
            #init vars
            itens = validated_data.pop('itens')
            request = self.context['request']
            #cria o log
            # gerando log do pedido com o agent e o ip da requisição
            log = Log.objects.create(
                browser=get_client_browser(request),
                remote_ip=get_client_ip(request)
            )
            #atualiza as informacoes do endereco
            endereco = validated_data.pop('endereco',None)
            if validated_data['delivery'] and endereco:
                validated_data.update(**self.recupera_dados_endereco(endereco))   
            
            #cria o pedido
            validated_data['cliente'] = get_user_lookup(request,'cliente')
            validated_data['log'] = log
            pedido = Pedido.objects.create(**validated_data)
            
            #cria o pedido dos itens
            self.gerar_itens_pedido(itens,pedido)
    
    def recupera_dados_endereco(self,endereco):
        """
        Retorna as informacacoes do endereco do cliente
        endereco: Endereco
        return: Dict
        """
        return {
            "cep": getattr(endereco, 'cep', None),
            "uf": getattr(endereco, 'uf', None),
            "logradouro": getattr(endereco, 'logradouro', None),
            "numero": getattr(endereco, 'numero', None),
            "complemento": getattr(endereco, 'complemento', None),
            "cidade": getattr(endereco, 'cidade', None),
            "bairro": getattr(endereco, 'bairro', None),
            "nome_endereco": getattr(endereco, 'nome_endereco', None),
            "nome_destinatario": getattr(endereco, 'nome_destinatario', None),
        }
    
    def gerar_itens_pedido(self,itens,pedido):
        """
        Gera os itens pedido de um pedido
        pedido: Pedido
        itens: List<OrderDict>
        return List<ItemPedido>
        """
        for item in itens:
            for apresentacao in item['apresentacao']:
                data_item_pedido = {}
                valor_unitario = 0
                apresentacao.get_manager.update_ranking_proposta(apresentacao.id)
                # Buscando o pmc base para calcular o valor unitário
                try:
                    tabela = apresentacao.tabelas.get(icms=cidade.uf.icms)
                    valor_unitario = tabela.pmc
                except Exception as err:
                    print(err)

                item_data['pedido'] = pedido
                item_data['valor_unitario'] = valor_unitario
                ItemPedido.objects.create(**item_data)