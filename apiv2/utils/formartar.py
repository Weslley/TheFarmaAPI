from api.utils.formats import formata_numero_apresentaca

def gerar_nome_dosagem(apresentacao):
    """
    Fortmata a apresentacao
    apresentacao: Apresentacao
    return: str
    """
    try:
        nome = ''
        if apresentacao.dosagem:
            dosagem = formata_numero_apresentaca(apresentacao.dosagem)
            nome += '{}{}'.format(dosagem,apresentacao.sufixo_dosagem.nome)
        if apresentacao.segunda_dosagem:
            dosagem = formata_numero_apresentaca(apresentacao.segunda_dosagem)
            nome += ' + {}{}'.format(dosagem,apresentacao.sufixo_segunda_dosagem)
        if apresentacao.terceira_dosagem:
            dosagem = formata_numero_apresentaca(apresentacao.terceira_dosagem)
            nome += ' + {}{}'.format(dosagem,apresentacao.sufixo_terceira_dosagem.nome)
        if apresentacao.quarta_dosagem:
            dosagem = formata_numero_apresentaca(apresentacao.quarta_dosagem)
            nome += ' + {}{}'.format(dosagem,apresentacao.sufixo_quarta_dosagem.nome)
        return nome
    except Exception as e:
        return apresentacao.nome