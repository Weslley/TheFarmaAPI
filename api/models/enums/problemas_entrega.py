class ProblemasEntrega():
    ENDERECO_NAO_ENCONTRADO = 1
    FALTA_ESTOQUE = 2
    DINHEIRO_ESTORNADO = 3

    @classmethod
    def get_text(cls,value):
        if value == cls.ENDERECO_NAO_ENCONTRADO:
            return 'endereço não encontrado'
        if value == cls.FALTA_ESTOQUE:
            return 'falta de estoque'
        if value == cls.DINHEIRO_ESTORNADO:
            return 'dinheiro foi estornado'