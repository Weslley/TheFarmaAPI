from api.utils.enum import IntEnum


class StatusPedido(IntEnum):
    """
    Enum para status do Pedido
    """
    ABERTO = 0
    ENVIADO = 1
    ENTREGUE = 2
    CANCELADO_PELA_FARMACIA = 3
    CANCELADO_PELO_CLIENTE = 4
