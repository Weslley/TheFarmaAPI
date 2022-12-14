from api.models.configuracao import Configuracao
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.enums.status_pedido import StatusPedido
from thefarmaapi._celery import app

from api.models.pedido import Pedido
from api.models.farmacia import Farmacia
from api.consumers import FarmaciaConsumer

from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal
import json

from api.utils.usuario_teste import check_user_eh_teste, fazer_proposta_faker

@app.task(queue='propostas')
def init_proposta(id_pedido):
    """
    Task para iniciar proposta
    :param id_pedido: Id do pedido
    :return:
    """
    try:
        duracao_proposta = Configuracao.objects.first().duracao_proposta
    except:
        duracao_proposta = timedelta(minutes=5)

    busca = True
    farmacias_enviadas = []
    rs_visualizadas = ''
    pedido = Pedido.objects.get(id=id_pedido)

    #verifica se eh o usuario teste
    if check_user_eh_teste(pedido.cliente.usuario):
        print('sim')
        pedido.gerar_proposta([Farmacia.objects.get(pk=8)])
        fazer_proposta_faker(pedido)
        return None
    else:
        print('nao')

    while busca:
        pedido = Pedido.objects.get(id=id_pedido)
        farmacias_proximas = Farmacia.objects.proximas(pedido)
        farmacias_sem_proposta = Farmacia.objects.proximas(pedido, exclude_farmacias=farmacias_enviadas)
        if farmacias_proximas:
            if farmacias_sem_proposta:
                farmacias_enviadas.extend(farmacias_sem_proposta)
                # gerando  propostas das farmacias
                pedido.gerar_proposta(farmacias_sem_proposta)
                # enviando para as farmaias selecionadas
                FarmaciaConsumer.send_propostas(pedido, farmacias_sem_proposta)
                #salva nos pedidos as farmacias que receberam
                for fa in farmacias_enviadas:
                    rs_visualizadas += str(fa.id) + ','
                pedido.farmacias_receberam = rs_visualizadas
                pedido.save()
        else:
            # Status Sem Proposta caso nao existam farmacias proximas
            pedido.status = StatusPedido.SEM_PROPOSTA
            pedido.save()
            return

        # verificando se ainda da tempo de buscar mais farmacias
        duracao = datetime.now() - pedido.log.data_criacao

        if duracao >= duracao_proposta or pedido.status != StatusPedido.ABERTO:
            busca = False
        else:
            sleep(5)

    pedido = Pedido.objects.get(id=id_pedido)
    if len(pedido.propostas) and pedido.status == StatusPedido.ABERTO:
        pedido.status = StatusPedido.TIMEOUT
    elif not len(pedido.propostas):
        pedido.status = StatusPedido.SEM_PROPOSTA

    pedido.save()

@app.task(queue='propostas')
def aplic_proposta_v2(pedido_id):
    """
    Metodo para fazer as propostas
    """ 
    #recupera o estado atual do pedido
    pedido = Pedido.objects.get(pk=pedido_id)
    #se tem proposta e continua com status aberto eh pq nao selecionou nenhuma
    total_propostas = len(pedido.propostas)
    if total_propostas and pedido.status == StatusPedido.ABERTO:
        pedido.status = StatusPedido.TIMEOUT
    elif not total_propostas:
        #nao recebeu uma proposta :(
        pedido.status = StatusPedido.SEM_PROPOSTA
    pedido.save()