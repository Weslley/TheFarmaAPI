from api.utils.enum import IntEnum


class StatusProduto(IntEnum):
    """
    Enum para status do Produto
    """
    REVISAR = 0
    PUBLICADO = 1
    NEGADO = 2
