from rest_framework import serializers
from api.models.pedido import Pedido, ItemPedido, ItemPropostaPedido
from api.models.endereco import Endereco
from api.serializers.log import LogSerializer
from django.db import transaction
from api.models.apresentacao import Apresentacao
from apiv2.utils.custom_fields import ListPrimaryKeyRelatoionField
from api.utils import get_client_browser, get_client_ip 
from api.models.log import Log
from api.utils import get_user_lookup, get_tempo_proposta
from api.models.farmacia import Farmacia
import itertools



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
            log = self.criar_log(request)
            #atualiza as informacoes do endereco
            endereco = validated_data.pop('endereco',None)
            if validated_data['delivery'] and endereco:
                validated_data.update(**self.recupera_dados_endereco(endereco))   
            
            #cria o pedido
            validated_data['cliente'] = get_user_lookup(request,'cliente')
            validated_data['log'] = log
            pedido = Pedido.objects.create(**validated_data)
            
            #cria o pedido dos itens
            rs = self.gerar_itens_pedido(itens,pedido)
            #gera as proposta
            farmacias_proximas = Farmacia.objects.proximas(pedido)
            self.gerar_proposta_permutada(itens,farmacias_proximas,pedido)
            return pedido

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
        rs = []
        for item in itens:
            for apresentacao in item['apresentacao']:
                #aumenta o hank de proposta
                apresentacao.get_manager.update_ranking_proposta(apresentacao.id)
                #data do item pedido
                data_item_pedido = {}
                data_item_pedido['pedido'] = pedido
                data_item_pedido['valor_unitario'] = self.get_pcm(apresentacao,pedido.cidade_obj)
                data_item_pedido['apresentacao'] = apresentacao
                rs.append(ItemPedido.objects.create(**data_item_pedido))
        return rs

    
    def criar_log(self,request):
        """
        Cria um log para o pedido
        request: Django Request
        return: Log
        """
        return Log.objects.create(
            browser=get_client_browser(request),
            remote_ip=get_client_ip(request)
        )
    
    def get_pcm(self,apresentacao,cidade):
        """
        Buscando o pmc base para calcular o valor unitário
        apresentacao: Apresentacao
        cidade: Cidade
        return: Decimal
        """
        valor_unitario = 0
        try:
            tabela = apresentacao.tabelas.get(icms=cidade.uf.icms)
            valor_unitario = tabela.pmc
        except Exception as err:
            print(err)
        return valor_unitario

    def parse_itens_lista_permutacao(self,item):
        """
        Faz o parse de uma lista para pode ser permutada
        item:dict
        return: List
        """
        lista = []
        quantidade = item['quantidade']
        return [{'quantidade':quantidade,'apresentacao':x} for x in item['apresentacao']]
    
    def gerar_proposta_permutada(self,itens,farmacias,pedido):
        """
        Gera proposta baseada na permutacao nas apresentacoes selecionadas
        itens: List<Dict>
        farmacias: List<Farmacia>
        pedido: Pedido
        return:
        """
        #permuta a lista de itens
        #fazendo antes o parse de dict para lista de dict
        lista_permutada = list(itertools.product(*map(self.parse_itens_lista_permutacao,itens)))
        for farmacia in farmacias:
            print('Interacao farmacia')
            for item_pedido in lista_permutada:
                for item in item_pedido:
                    print(farmacia,item)
                    ItemPropostaPedido.objects.create(
                        pedido=pedido,
                        valor_unitario=0,
                        quantidade=item['quantidade'],
                        apresentacao=item['apresentacao'],
                        farmacia=farmacia
                    )
    
        import pdb; pdb.set_trace()