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

def desformatar_nome_dosagem(nome):
    """
    Metodo que reverte o nome de uma dosagem
    nome: str
    return: List<Dict>
    """
    rs = []
    lista = nome.split(' + ')
    for item in lista:
        dosagem, sufixo = split_numero_string(item)
        rs.append({
            'dosagem': dosagem,
            'sufixo': sufixo
        })
    return sufixo

def split_numero_string(setencia):
    """
    Divide uma sentencia em string e numero. Obs: Essa sequencia deve ser seguida e o numero primeiro
    ex: 123abc retorno sera (123,abc)
    setencia: str
    return: Tuple
    """
    i = 0
    for c in setencia:
        if c.isdigit():
            i += 1
        else:
            return (setencia[0:i+1],setencia[i+1:])
