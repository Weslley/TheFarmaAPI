from hashlib import md5


def make_md5(value, encoding='utf-8'):
    """
    Método que recebe uma string e retorna o MD5 referente
    :return: str
    """
    return md5(value.encode(encoding)).hexdigest()
