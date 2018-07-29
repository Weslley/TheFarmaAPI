from api.utils.enum import IntEnum


class TipoNotificacao(IntEnum):
    AVISO = 0
    HOME = 1
    PRODUTO = 2
    PEDIDO = 3
    PROMOCAO = 4
