from api.utils.enum import IntEnum


class StatusPedido(IntEnum):
    """
    Enum para status do Pedido
    """
    ABERTO = 0                        # Aguardando propostas
    ACEITO = 1                        # Proposta selecionada foi aceita
    AGUARDANDO_ENVIO_FARMACIA = 2     # Caso a farmacia for enviar
    AGUARDANDO_RETIRADA_CLIENTE = 3   # Caso o cliente for retirar o produto na farmacia
    ENVIADO = 4                       # Quando o mesmo for enviado pela farmacia
    ENTREGUE = 5                      # Quando for feito a confirmação de entrega
    CANCELADO_PELA_FARMACIA = 6       # Cancelamento pela farmacia - FEITO SOMENTE PELOS ADMINISTRADORES
    CANCELADO_PELO_CLIENTE = 7        # Quando o cliente não aceita a proposta
    SEM_PROPOSTA = 8                  # Caso na tenha sido encontrado uma proposta para o cliente
    TIMEOUT = 9                       # Timeout para aceitar a proposta
    NAO_ENTREGUE = 10                 # Farmacia nao conseguiu entregar um pedido
    ESTORNADO = 11