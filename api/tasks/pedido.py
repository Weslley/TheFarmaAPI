from api.models.configuracao import Configuracao
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
    while busca:
        # Atualizando pedido
        pedido = Pedido.objects.get(id=id_pedido)
        # selecionando as farmacias proximas
        farmacias = Farmacia.objects.proximas(pedido, exclude_farmacias=farmacias_enviadas)
        if farmacias:
            farmacias_enviadas.extend(farmacias)
            # gerando  propostas das farmacias
            pedido.gerar_proposta(farmacias)
            # enviando para as farmaias selecionadas
            FarmaciaConsumer.send_propostas(pedido, farmacias)

        # verificando se ainda da tempo de buscar mais farmacias
        duracao = datetime.now() - pedido.log.data_criacao
        if duracao >= duracao_proposta or pedido.status != StatusPedido.ABERTO:
            busca = False
        else:
            sleep(5)
