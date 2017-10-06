from api.utils.enum import IntEnum


class StatusItem(IntEnum):
    ABERTO = 0
    ENVIADO = 1
    ENTREGUE = 2
    CANCELADO = 3
