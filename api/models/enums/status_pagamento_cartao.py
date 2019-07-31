from api.utils.enum import IntEnum


class StatusPagamentoCartao(IntEnum):
    """
    Representação do status do pedido
    """
    NAO_FINALIZADO = 0
    AUTORIZADO = 1
    PAGAMENTO_CONFIRMADO = 2
    NEGADO = 3
    CANCELADO = 10
    ESTORNADO = 11
    PENDENTE = 12
    ABORTADA = 13
    AGENDADA = 20
    PAGAMENTO_CANCELADO = 11

# CHOICES = (
#     (IDENTIFICACAO, 'IDENTIFICAÇÃO'),
#     (ENDERECO, 'ENDEREÇO'),
#     (PAGAMENTO, 'PAGAMENTO'),
#     (CONFIRMACAO, 'CONFIRMAÇÃO'),
#     (FINALIZADO, 'FINALIZADO'),
# )
