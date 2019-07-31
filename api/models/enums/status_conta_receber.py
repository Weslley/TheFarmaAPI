from api.utils.enum import IntEnum


class StatusContaReceber(IntEnum):
    """
    Status de contas a receber
    """
    ABERTA = 0
    PAGA = 1
    CANCELADA = 2
