from api.utils.enum import IntEnum


class StatusPagamentoCartao(IntEnum):
    """
    Representação do status do pedido
    """
    NOT_FINISHED = 0
    AUTHORIZED = 1
    PAYMENT_CONFIRMED = 2
    DENIED = 3
    VOIDED = 10
    REFUNDED = 11
    PENDING = 12
    ABORTED = 13
    SCHEDULED = 20

# CHOICES = (
#     (IDENTIFICACAO, 'IDENTIFICAÇÃO'),
#     (ENDERECO, 'ENDEREÇO'),
#     (PAGAMENTO, 'PAGAMENTO'),
#     (CONFIRMACAO, 'CONFIRMAÇÃO'),
#     (FINALIZADO, 'FINALIZADO'),
# )
