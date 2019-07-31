from api.utils.enum import IntEnum


class StatusItem(IntEnum):
    ABERTO = 0
    CONFIRMADO = 1
    ENVIADO = 2
    ENTREGUE = 3
    CANCELADO = 4
