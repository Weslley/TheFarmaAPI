import re


class Converter:
    """
    Classe com metodos de conversão
    """

    @classmethod
    def snake_case(cls, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
