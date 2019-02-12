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
