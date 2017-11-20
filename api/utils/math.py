import math


def truncate(value, places=1, _type=float):
    """
    truncate number without round
    :param value: Valor a ser truncado
    :param places: Casa decimais
    :return:
    """
    return math.floor(value * 10 ** places) / 10 ** places
