import itertools

from itertools import groupby

from django.db import transaction
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Sum, Case, When, Q, IntegerField

from rest_framework import serializers

from api.models.log import Log
from api.models.produto import Produto
from api.models.endereco import Endereco
from api.models.farmacia import Farmacia
from api.models.apresentacao import Apresentacao
from api.models.pedido import Pedido, ItemPedido, ItemPropostaPedido
from api.models.enums.status_item_proposta import StatusItemProposta

from api.serializers.log import LogSerializer
from api.serializers.pedido import PedidoDetalhadoSerializer
from api.serializers.farmacia import FarmaciaEnderecoSerializer
from api.serializers.pedido import ItemPropostaSimplificadoSerializer

from api.utils import get_client_browser, get_client_ip 
from api.utils import get_user_lookup, get_tempo_proposta

from api.consumers.farmacia import FarmaciaConsumer, PropostaSerializer, ItemPropostaSerializer

from apiv2.utils.formartar import desformatar_nome_dosagem
from apiv2.utils.custom_fields import ListPrimaryKeyRelatoionField

from apiv2.serializers.farmacia import FarmaciaPedidoSerializer

class ItensPropostaPermutadosSerializer(PropostaSerializer):

    def get_itens_proposta(self,obj):
        itens = self.context['lista']
        context = {
            'cidade': self.context['farmacia'].endereco.cidade,
        }
        itens_proposta = ItemPropostaSerializer(
            many=True,
            instance=itens,
            context=context
        )
        return itens_proposta.data


class ItemPedidoCreateSerializer(serializers.Serializer):
    apresentacao = serializers.PrimaryKeyRelatedField(queryset=Apresentacao.objects.all(),required=False)
    quantidade = serializers.IntegerField()
    produto = serializers.CharField(required=False)
    generico = serializers.BooleanField(write_only=True)
    dosagens = serializers.ListField(required=False)
    embalagem = serializers.CharField(required=False)
    quantidade_embalagem = serializers.DecimalField(required=False,max_digits=10,decimal_places=2)
    sufixo_quantidade = serializers.CharField(required=False,allow_blank=True,allow_null=True)

    def validate(self,data):
        if not 'apresentacao' in data:
            raise serializers.ValidationError({'detail':'Por favor informe uma apresentacao'})
        
        return data

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
            pedido = Pedido(**validated_data)

            #cria um atributo para poder ignorar o signal
            pedido._ignore_signal = True

            #salva realemnte em banco
            pedido.save()

            #cria os itens do pedido
            rs = self.gerar_itens_pedido(itens, pedido)

            #gera as proposta
            farmacias_proximas = Farmacia.objects.proximas(pedido)
            self.gerar_proposta_permutada(itens, farmacias_proximas, pedido)

            return pedido

    def recupera_dados_endereco(self, endereco):
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
        i = 0
        for item in itens:
            #calcula o valor_unitario da primeira apresentacao e coloca no dict original
            #futuramente usado no valor_unitario da proposta
            itens[i].update({'valor_unitario':0})

            #add as apresentacoes
            #if item['generico']:
                #item['apresentacao'] = self.get_apresentacoes_produto(item)

            i+=1
            #convert pra lista
            if isinstance(item['apresentacao'], Apresentacao):
                item['apresentacao'] = [item['apresentacao'],]

            for apresentacao in item['apresentacao']:
                #aumenta o hank de proposta
                apresentacao.get_manager.update_ranking_proposta(apresentacao.id)
                #data do item pedido
                data_item_pedido = {}
                data_item_pedido['quantidade'] = item['quantidade']
                data_item_pedido['pedido'] = pedido
                data_item_pedido['valor_unitario'] = self.get_pcm(apresentacao, pedido.cidade_obj)
                data_item_pedido['apresentacao'] = apresentacao
                data_item_pedido['aceita_generico'] = item['generico']
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
    
    def get_pcm(self,apresentacao, cidade):
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
        Faz um lista para cada apresentacao replicando as informacoe de qtd e valor_unitario
        item:dict
        return: List
        """
        quantidade = item['quantidade']
        valor_unitario = item['valor_unitario']
        apresentacao_pedida = item['apresentacao_pedida']
        return [{ 'quantidade': quantidade, 'apresentacao': x, 'valor_unitario': valor_unitario, 'apresentacao_pedida': apresentacao_pedida } for x in item['apresentacao']]
    
    def gerar_proposta_permutada(self, itens, farmacias, pedido):
        """
        Gera proposta baseada na permutacao nas apresentacoes selecionadas
        itens: List<Dict>
        farmacias: List<Farmacia>
        pedido: Pedido
        return:
        """
        itens_pedidos = []
        for item in itens:
            item['apresentacao_pedida'] = item['apresentacao'][0]
            if item['generico']:
                item['apresentacao'] = self.get_apresentacoes_produto(item)
            itens_pedidos.append(item)

        #permuta a lista de itens
        #fazendo antes o parse de dict para lista de dict
        lista_permutada = list(itertools.product(*map(self.parse_itens_lista_permutacao, itens_pedidos)))
        
        print(lista_permutada)
        for farmacia in farmacias:
            #controle de qual foi o id da permutacao
            i = 0
            #para cada farmacia cria propostas permutadas
            # print('Interacao farmacia:')
            for item_pedido in lista_permutada:
                #pedidos da proposta
                itens_proposta = []
                i += 1
                for item in item_pedido:
                    #cria o item pedidos
                    itens_proposta.append(ItemPropostaPedido.objects.create(
                        pedido=pedido,
                        valor_unitario=item['valor_unitario'],
                        quantidade=item['quantidade'],
                        apresentacao=item['apresentacao'],
                        farmacia=farmacia,
                        apresentacao_pedida=item['apresentacao_pedida'],
                        permutacao_id=i
                    ))

                #serializa a proposta atual
                data = self.serializer_data_item_pedido_proposta(itens_proposta, pedido, farmacia)

                #manda para o ws
                print("Permutação =>", i)
                print("Farmacia =>", farmacia.id)
                print(data)
                FarmaciaConsumer.send(data ,**{'id': farmacia.id})


    def serializer_data_item_pedido_proposta(self,lista,pedido,farmacia):
        """
        Serializa os dados para mandar pelo websocket para as farmacias
        lista: List<ItemPropostaPedido>
        pedido: Pedido
        farmacia: Farmacia
        return: Dict
        """
        serializer = ItensPropostaPermutadosSerializer(pedido,context={'lista':lista,'farmacia':farmacia})
        return serializer.data
    
    def get_apresentacoes_produto(self, item):
        """
        Recupera as apresentacoes de um produto baseado nas suas especificacoes
        item: Dict{produto,embalagem,quantidade_embalagem,sufixo_quantidade,dosagens}
        return: List<Apresentacoes>
        """
        #apresentacao = Apresentacao.objects.get(id =item['apresentacao'].id)
        apresentacao = item['apresentacao'][0]
        genericos = []
        genericos.append(apresentacao)

        for ap in apresentacao.genericos(True):
            if apresentacao.dosagem_formatada == ap.dosagem_formatada:
                genericos.append(ap)

        return genericos


class PropostasFarmaciaSerializer(serializers.ModelSerializer):
    farmacia = serializers.SerializerMethodField()
    permutacao_id = serializers.SerializerMethodField()
    possui_todos_itens = serializers.SerializerMethodField()
    itens = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()
    valor_frete = serializers.SerializerMethodField()
    valor_total_com_frete = serializers.SerializerMethodField()
    quantidade_maxima_parcelas = serializers.SerializerMethodField()

    class Meta:
        model = Farmacia
        fields = (
            'farmacia',
            'permutacao_id',
            'possui_todos_itens',
            'itens',
            'status',
            'valor_total',
            'valor_frete',
            'valor_total_com_frete',
            'quantidade_maxima_parcelas'
        )
    
    def get_farmacia(self,obj):
        serializer = FarmaciaPedidoSerializer(obj,context=self.context)
        return serializer.data

    def get_permutacao_id(self,obj):
        try:
            return self.context['permutacao_id']
        except Exception as err:
            return None
    
    def get_possui_todos_itens(self,obj):
        return obj.possui_todos_itens_permutacao(
            self.context['pedido'],
            self.context['permutacao_id']
        )

    def get_itens(self,obj):
        itens = obj.get_itens_proposta_permutacao(self.context['pedido'], self.context['permutacao_id'])
        serializer = ItemPropostaSimplificadoSerializer(itens, many=True)
        return serializer.data
    
    def get_status(self,obj):
        return obj.get_status_proposta_permutacao(
            self.context['pedido'],
            self.context['permutacao_id']
        )
    
    def get_valor_total(self,obj):
        return obj.get_valor_proposta_permutacao(
            self.context['pedido'],
            self.context['permutacao_id']
        )

    def get_valor_total_com_frete(self,obj):
        return obj.get_valor_proposta_permutada_com_frete(
            self.context['pedido'],
            self.context['permutacao_id']
        )
    
    def get_quantidade_maxima_parcelas(self,obj):
        return obj.get_quantidade_maxima_parcelas(self.context['pedido'])
    
    def get_valor_frete(self,obj):
        return obj.get_valor_frete(self.context['pedido'])


class PedidoRetriveSerializer(PedidoDetalhadoSerializer):

    def get_propostas(self,obj):
        """
        Recupera as melhores propostas que um pedido recebeu
        obj: Pedido
        return: List
        """
        propostas = obj.itens_proposta.filter(status=StatusItemProposta.ENVIADO)\
            .values('permutacao_id','farmacia_id')\
            .annotate(
                total_proposta=Sum(ExpressionWrapper(F('quantidade')*F('valor_unitario'),output_field=DecimalField())),
                total_possui=Sum(Case(
                    When(Q(possui=True),then=1),
                    When(Q(possui=False),then=0),
                    output_field=IntegerField()
                ))
            ).order_by('-total_possui','farmacia_id','total_proposta')
        
        #agrupa por farmacia_id
        melhores_propostas = []
        for key, group in groupby(list(propostas), key=lambda x:x['farmacia_id']):
            #converte para lista e pega o primeiro
            #como ja vem ordenado pelo banco
            #o primeiro eh o que possui mais itens e tem o menor preco
            for x in list(group):
                if(x['total_proposta']!=0):
                    melhores_propostas.append(PropostasFarmaciaSerializer(Farmacia.objects.get(id=x['farmacia_id']), context={ 'pedido':obj, 'permutacao_id': x['permutacao_id'] }).data)

            #instancia o serializer da proposta da farmacia passando o pedido e permutacao
            #ja chama o data tambem
        
        return melhores_propostas
        