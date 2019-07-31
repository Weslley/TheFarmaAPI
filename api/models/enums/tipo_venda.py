from api.utils.enum import IntEnum


class TipoVenda(IntEnum):
    SEM_RECEITA = 0
    COM_RECEITA = 1
    NAO_PERMITIDA = 2
