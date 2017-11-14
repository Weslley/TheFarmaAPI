from decimal import Decimal

from api.models.configuracao import Configuracao
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.enums.status_pedido import StatusPedido
from thefarmaapi._celery import app
from api.models.pedido import Pedido
from api.models.farmacia import Farmacia
from api.consumers import FarmaciaConsumer
from time import sleep
from datetime import datetime, timedelta


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

    # alteração para globo
    queryset = Farmacia.objects.order_by('-data_criacao')[:2]
    farmacias = [f for f in queryset]
    pedido = Pedido.objects.get(id=id_pedido)
    if farmacias:
        farmacias_enviadas.extend(farmacias)
        # gerando  propostas das farmacias
        pedido.gerar_proposta(farmacias)

        # Selecionando ramdomicamente uma das farmacias
        # para dar um desconto(randomico) em produtos
        import random
        farmacia_id = random.choice([f.id for f in farmacias])
        for item in pedido.itens_proposta.filter(farmacia_id=farmacia_id):
            # escolhendo aleatoriamente um desconto
            if item.valor_unitario >= Decimal(1):
                item.valor_unitario -= ((Decimal(random.choice([15, 20, 25, 30]) / 100)) * item.valor_unitario)
                item.save()

        # marcando como enviado
        for item in pedido.itens_proposta.all():
            item.status = StatusItemProposta.ENVIADO
            item.possui = True
            item.save()

    # passando o tempo
    while busca:
        # verificando se ainda da tempo de buscar mais farmacias
        duracao = datetime.now() - pedido.log.data_criacao
        if duracao >= duracao_proposta or pedido.status != StatusPedido.ABERTO:
            busca = False
        else:
            sleep(5)

    # while busca:
    #     # Atualizando pedido
    #     pedido = Pedido.objects.get(id=id_pedido)
    #     # selecionando as farmacias proximas
    #     farmacias = Farmacia.objects.proximas(pedido, exclude_farmacias=farmacias_enviadas)
    #     if farmacias:
    #         farmacias_enviadas.extend(farmacias)
    #         # gerando  propostas das farmacias
    #         pedido.gerar_proposta(farmacias)
    #         # enviando para as farmaias selecionadas
    #         FarmaciaConsumer.send_propostas(pedido, farmacias)
    #
    #     # verificando se ainda da tempo de buscar mais farmacias
    #     duracao = datetime.now() - pedido.log.data_criacao
    #     if duracao >= duracao_proposta or pedido.status != StatusPedido.ABERTO:
    #         busca = False
    #     else:
    #         sleep(5)

    pedido = Pedido.objects.get(id=id_pedido)
    if len(pedido.propostas) and pedido.status == StatusPedido.ABERTO:
        pedido.status = StatusPedido.TIMEOUT
    elif not len(pedido.propostas):
        pedido.status = StatusPedido.SEM_PROPOSTA

    pedido.save()
