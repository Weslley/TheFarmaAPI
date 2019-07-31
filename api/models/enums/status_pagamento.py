from api.utils.enum import IntEnum


class StatusPagamento(IntEnum):
    """
    Representação do status do pagamento do pedido
    """
    ABERTO = 0
    PAGO = 1
    CANCELADO = 2
