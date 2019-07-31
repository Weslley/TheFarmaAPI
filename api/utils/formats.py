def formata_numero_apresentaca(value):
    """
    Corrigue a formatacao do numero da formatacao
    value: Decimal
    return: String
    """
    value = str(value)
    aux = value.split('.')
    casas_decimais = aux[1]
    casas_decimais = casas_decimais.replace('0','')
    if casas_decimais:
        return '{}{}'.format(aux[0],casas_decimais)
    else:
        return '{}'.format(aux[0])

def formatar_telefone(value):
    """
    Formata um telefone
    value: String
    return: String
    """
    try:
        if len(value) == 11:
            return '({}) {}-{}'.format(value[0:2],value[2:7],value[7:])
        if len(value) == 10:
            return '({}) {}-{}'.format(value[0:2],value[2:6],value[6:])
        return value
    except Exception as e:
        print(str(e))
        return value