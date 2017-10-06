import linecache
import re
from datetime import timedelta, datetime
from types import MethodType

import sys

from api.models.configuracao import Configuracao


class Converter:
    """
    Classe com metodos de conversão
    """

    @classmethod
    def snake_case(cls, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_client_ip(request):
    """
    Retorna o IP da requisição
    :param request: Request
    :return: Ip da mesma
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    """
    Retorna o Agent(Browser) da requisição
    :param request: Request
    :return: Agent
    """
    agent = request.META.get('HTTP_USER_AGENT')
    return agent


def get_user_lookup(request, lookup):
    """
    Retorna o objeto passado como lookup
    :param request: Request
    :param lookup: String do nome do lookup
    :return: Objeto relacionado ao user
    """
    if hasattr(request.user, lookup):
        return getattr(request.user, lookup, None)
    return None


def methodize(func, instance):
    """
    Set function in instance method of a class
    :param func: Function
    :param instance: Instance
    :return: method function
    """
    return MethodType(func, instance)


def calcula_distancia(point_1, point_2):
    """
    Calcula distancia entre coordenadas em quilometros
    :param point_1: Tupla de latitude e longitude (lat, long)
    :param point_2: Tupla de latitude e longitude (lat, long)
    :return: distancia em quilomentros
    """
    from geopy.distance import vincenty
    return vincenty(point_1, point_2).kilometers


def get_tempo_proposta(pedido):
    """
    Metodo que retorna o tempo que falta para pedido ser definido nas farmacias
    :param pedido: Pedido
    :return: Tempo em segundos
    """
    try:
        duracao_proposta = Configuracao.objects.first().duracao_proposta
    except Exception:
        duracao_proposta = timedelta(minutes=5)

    tempo = (duracao_proposta - (datetime.now() - pedido.log.data_criacao)).total_seconds()
    return tempo if tempo >= 0 else 0


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))