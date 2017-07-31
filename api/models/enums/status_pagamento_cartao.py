from api.utils.enum import IntEnum


class StatusPagamentoCartao(IntEnum):
    """
    Representação do status do pedido
    """
    IDENTIFICACAO = 0
    ENDERECO = 1
    PAGAMENTO = 2
    CONFIRMACAO = 3
    FINALIZADO = 4

# CHOICES = (
#     (IDENTIFICACAO, 'IDENTIFICAÇÃO'),
#     (ENDERECO, 'ENDEREÇO'),
#     (PAGAMENTO, 'PAGAMENTO'),
#     (CONFIRMACAO, 'CONFIRMAÇÃO'),
#     (FINALIZADO, 'FINALIZADO'),
# )
