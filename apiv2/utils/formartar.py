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
