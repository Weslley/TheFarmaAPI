import locale

#ativa o locale br huehue
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_dinheiro(value):
    """
    Formata um valor para o padrao br
    value: Decimal
    padrao: String
    """
    return locale.currency(value,grouping=True)