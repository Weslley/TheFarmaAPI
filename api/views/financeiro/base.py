from django.db.models import Q, Sum
from rest_framework import generics,permissions, status
from rest_framework.response import Response

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta import Conta
from api.models.pedido import Pedido, LogData, ItemPropostaPedido, ItemPedido
from api.models.enums.status_pedido import StatusPedido
from api.serializers.conta import ContaMinimalSerializer
from api.serializers.pedido import PedidoTotaisSerializer, \
    PedidoMinimalSerializer, LogDataSerializer, VendaPedido
from api.serializers.medicamento import MedicamentoRelatorio
from django.db.models import F, Q
from datetime import datetime, date
from django.db.models import FloatField
import calendar
import locale
from itertools import groupby
import decimal
from api.utils.geo import get_pedidos_in_radius, get_mais_visualizados
from api.models.farmacia import Farmacia
from api.models.enums.status_pedido_faturamento import StatusPedidoFaturamento
from api.models.enums.forma_pagamento import FormaPagamento
from api.models.enums.status_conta import StatusConta


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def get_ultima_conta(representante):
    """
    Recupera o valor total dos que naoa  foram faturados
    representante: Representante
    return: Dict
    """
    #prepara o retorno
    valor_total = 0
    rs = {'valor_total':0,'tipo':StatusConta.RECEBER}
    #todos os pedidos nao faturados e status de entregue
    pedidos = Pedido.objects.filter(
        farmacia__representantes=representante,
        status_faturamento=StatusPedidoFaturamento.NAO_FATURADO,
        status=StatusPedido.ENTREGUE
    )
    #calcula o valor da conta
    for pedido in pedidos:
        if pedido.forma_pagamento == FormaPagamento.CARTAO:
            valor_total += pedido.valor_liquido
            valor_total -= pedido.valor_comissao_thefarma
        elif pedido.forma_pagamento == FormaPagamento.DINHEIRO:
            valor_total -= pedido.valor_comissao_thefarma
        if valor_total > 0:
            rs.update({'valor_total':valor_total,'tipo':StatusConta.PAGAR})
        else:
            rs.update({'valor_total':valor_total,'tipo':StatusConta.RECEBER})
    return rs
    
def paginar_resultado(query,page):
    quantidade = 15
    return query[quantidade*page:quantidade*(page+1)]

class ResumoListagemVendas(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Resumo da listagem de vendas
    """
    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        params = request.query_params
        flag = True
        filtro = {}

        if params.get('mes'):
            data_ref = datetime.strptime(params.get('mes'), '%B')
            filtro.update(
                {'data_criacao__month': data_ref.month}
            )
            flag = False

        if params.get('ano'):
            filtro.update(
                {'data_criacao__year': params.get('ano')}
            )
            flag = False

        if flag:
            hoje = datetime.now()
            filtro = {
                'data_criacao__year': hoje.year,
                'data_criacao__month': hoje.month,
                'data_criacao__day': hoje.day
            }

        pedidos_do_periodo = Pedido.objects\
            .filter(
                status=StatusPedido.ENTREGUE,
                farmacia__representantes=representante,
                **filtro
            )

        valores_pedidos = pedidos_do_periodo.aggregate(
            bruto=Sum('valor_bruto'),
            liquido=Sum('valor_liquido')
        )

        logs = LogData.objects.filter(farmacia__representantes=representante)

        for k, v in valores_pedidos.items():
            if v == None:
                valores_pedidos[k] = 0

        data = {
            'periodos': LogDataSerializer(logs, many=True).data,
            'resumo': {
                'valor_bruto': valores_pedidos.get('bruto'),
                'valor_liquido': valores_pedidos.get('liquido'),
                'quantidade': pedidos_do_periodo.count()
            },
            'data': PedidoMinimalSerializer(pedidos_do_periodo, many=True).data,
        }
        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class ResumoFinanceiro(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):

    def get(self, request, *args, **kwargs):
        representante = self.get_object()

        # Filtrando as ultimas 4 vendas
        contas = Conta.objects.filter(
            farmacia__representantes=representante
        ).order_by('-data_vencimento')

        hoje = datetime.now()
        pedidos_de_hoje = Pedido.objects\
            .filter(
                status=StatusPedido.ENTREGUE,
                farmacia__representantes=representante,
                data_criacao__year=hoje.year,
                data_criacao__month=hoje.month,
                data_criacao__day=hoje.day
            )\
            .aggregate(
                bruto=Sum('valor_bruto'),
                liquido=Sum('valor_liquido')
            )

        # Valores calculados de rendimento de cada mês
        values = []
        for mes in range(1, 13):
            query = Pedido.objects\
                .filter(
                    status=StatusPedido.ENTREGUE,
                    data_criacao__month=mes,
                    data_criacao__year=date.today().year,
                    farmacia__representantes=representante,
                )\
                .aggregate(total=Sum('valor_bruto'))

            valor = float(query['total']) if query['total'] else 0
            values.append(valor)
        
        #monta a reposta 
        ult_conta = get_ultima_conta(representante)
        print(ult_conta)
        data = {
            'conta_atual': {
                'tipo':ult_conta['tipo'],
                'valor_total':ult_conta['valor_total'],
                'data_vencimento':contas.first().data_vencimento,
                'id':contas.first().id,
                'status':contas.first().status,
            },
            'contas': ContaMinimalSerializer(contas[:6], many=True).data,
            'vendas_hoje': PedidoTotaisSerializer(pedidos_de_hoje, many=False).data,
            'rendimentos': {
                'labels': [n.upper() for n in calendar.month_name if n],
                'values': values
            }
        }

        return Response(data)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class MedicamentosMaisVendidos(generics.GenericAPIView):
    """
    Recupera as vendas dos medicamentos
    recebe via parametro url(mes,ano)
    """


    def get(self,request,*args, **kwargs):
        #int vars
        mes = self.request.GET.get('mes',None)
        page = int(self.request.GET.get('page',0))
        ano = self.request.GET.get('ano',None)
        #filtros para as datas das querys
        filtros_pedido = {
            'data_criacao__year':ano,
            'data_criacao__month':mes,
        }
        filtros_itens_pedido = {
            'pedido__data_criacao__year':ano,
            'pedido__data_criacao__month':mes,
        }
        #se nao for passado nada, seta como o dia o filtro das datas
        if not (mes and ano):
            hoje = datetime.now()
            mes = hoje.month
            ano = hoje.year
            dia = hoje.day
            filtros_pedido.update({'pedido__data_criacao__day':dia})
            filtros_itens_pedido.update({'pedido__data_criacao__day':dia})
            
        representante = self.get_object()
        medicamentos = []
        quantidade = 0
        valor_bruto = 0
        valor_liquido = 0

        #pega todos os pedidos entregues
        pedidos = Pedido.objects.filter(
            status=StatusPedido.ENTREGUE,
            farmacia__representantes=representante,
            **filtros_pedido
        )

        #intera nos itens dos pedidos que a farmacia vendeu
        itens_pedido = ItemPedido.objects.filter(
            pedido__status=StatusPedido.ENTREGUE,
            pedido__farmacia__representantes=representante,
            **filtros_itens_pedido
        )\
        .annotate(
            valor_liquido=Sum(F('quantidade_atendida') * F('valor_unitario'),output_field=FloatField()),
            valor_bruto=Sum(F('quantidade') * F('valor_unitario'),output_field=FloatField())
        )\
        .values(
            'valor_liquido',
            'valor_bruto',
            'quantidade',
            'apresentacao__codigo_barras',
            'apresentacao__produto__id',
            'apresentacao__produto__nome',
            'apresentacao__produto__laboratorio__nome',
        ).order_by('apresentacao__produto__id')

        #calcula o total bruto e liquido
        valores = itens_pedido.aggregate(bruto=Sum('valor_bruto'),liquido=Sum('valor_liquido'))

        itens_pedido = paginar_resultado(itens_pedido,page)

        #agrupa
        for key, group in groupby(list(itens_pedido), key=lambda x:x['apresentacao__produto__id']):
            for item in group:
                quantidade += item['quantidade']
                valor_liquido += item['valor_liquido']
                valor_bruto += item['valor_bruto']
            #acabou o produto add no medicamentos
            medicamentos.append({
                'valor_liquido':valor_liquido,
                'valor_bruto':valor_bruto,
                'quantidade':quantidade,
                'id':item['apresentacao__produto__id'],
                'nome_produto':item['apresentacao__produto__nome'],
                'fabricante':item['apresentacao__produto__laboratorio__nome'],
                'codigo_barras':item['apresentacao__codigo_barras'],
            })
            #resetar
            quantidade = 0
            valor_bruto = 0
            valor_liquido = 0

        return Response({
            'total_numero_vendas':len(pedidos),
            'total_liquido':'{}'.format(locale.currency(valores['liquido'])),
            'total_bruto':'R$ {}'.format(locale.currency(valores['bruto'])),
            'medicamentos':medicamentos
        })
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia

class MedicamentosMaisVendidosDetalhes(generics.GenericAPIView):
    """
    recupera detalhes das vendas de um produto
    recebe via parametro url(mes,ano)
    """

    def get(self,request,*args, **kwargs):
        representante = self.get_object()
        mes = request.GET.get('mes',None)
        ano = request.GET.get('ano',None)
        rs_vendas = []
        valor_liquido = decimal.Decimal(0)
        valor_bruto = decimal.Decimal(0)
        id = self.kwargs.get('id')
        if not (mes and ano):
            mes = datetime.now().month
            ano = datetime.now().year
        
        #recupera todas os pedidos que contem o medicamento
        itens_pedido = ItemPedido.objects.filter( 
            Q(pedido__farmacia__representantes=representante) \
            & Q(pedido__data_criacao__year=ano)\
            & Q(pedido__data_criacao__month=mes)\
            & Q(apresentacao__produto__id=id)
        )

        for item in itens_pedido:
            valor_liquido += item.total_liquido
            valor_bruto += item.total_bruto

        #monta todas as vendas
        for item in itens_pedido:
            rs_vendas.append(VendaPedido(item).data)
        
        return Response({
            'total_vendas':len(itens_pedido),
            'total_liquido':locale.currency(valor_liquido),
            'total_bruto':locale.currency(valor_bruto),
            'nome_produto':itens_pedido[0].apresentacao.produto.nome,
            'vendas':rs_vendas,
        })
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class MaisVendidosNaRegiao(generics.GenericAPIView):
    """
    relatorio de medicamentos mais pedidos na regiao da farmacia
    """

    def get(self,request,*args, **kwargs):
        representante = self.get_object()
        mes = request.GET.get('mes',None)
        ano = request.GET.get('ano',None)
        farmacia = Farmacia.objects.get(representantes=representante)
        #verifica se foi passado
        if not (mes and ano):
            pedidos = get_pedidos_in_radius(farmacia.latitude,farmacia.longitude,farmacia.id,6,StatusPedido.ENTREGUE,hoje=True)
        else:
            #cria o range de datas
            data_inicio = datetime(int(ano),int(mes),1)
            try:
                data_final = datetime(int(ano),int(mes),31)
            except:
                data_final = datetime(int(ano),int(mes),30)
                if mes == 2:
                    data_final = datetime(int(ano),int(mes),28)
            pedidos = get_pedidos_in_radius(farmacia.latitude,farmacia.longitude,6,farmacia.id,StatusPedido.ENTREGUE,data_final=data_final,data_inicio=data_inicio,hoje=False)
        
        #recupera os pedidos
        return Response(pedidos)
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia


class MaisPesquisadoNoRaio(generics.GenericAPIView):
    """
    Recupero os mais pequisados na regiao
    """

    def get(self,request, *args, **kwargs):
        representante = self.get_object()
        ano = self.request.GET.get('ano',None)
        mes = self.request.GET.get('mes',None)
        page = int(self.request.GET.get('page',0))
        farmacia = Farmacia.objects.get(representantes=representante)
        if not (mes and ano):
            hoje = True
            pedidos = get_mais_visualizados(farmacia.latitude,farmacia.longitude,6,page=page,hoje=hoje)
        else:
            #cria o range de datas
            data_inicio = datetime(int(ano),int(mes),1)
            try:
                data_final = datetime(int(ano),int(mes),31)
            except:
                data_final = datetime(int(ano),int(mes),30)
                if mes == 2:
                    data_final = datetime(int(ano),int(mes),28)
            pedidos = get_mais_visualizados(farmacia.latitude,farmacia.longitude,6,page=page,data_final=data_final,data_inicio=data_inicio)
        #recupera a lista de pesquisados 
        

        return Response(pedidos)
    
    
    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia
