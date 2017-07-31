import enum
from enum import IntEnum as _IntEnum, Enum as _Enum


@enum.unique
class IntEnum(_IntEnum):
    """
    Classe de enum com metodo para choices, utilizado em coiche fields Django
    """

    @classmethod
    def choices(cls):
        """
        Metodo que retorna uma lista de tuplas (NAME, VALUE) do itens do Enum
        :return: lista de tuplas (NAME, VALUE)
        """
        return [(n.name, n.value) for n in cls]


@enum.unique
class Enum(_Enum):
    """
    Classe de enum com metodo para choices, utilizado em coiche fields Django
    """

    @classmethod
    def choices(cls):
        """
        Metodo que retorna uma lista de tuplas (NAME, VALUE) do itens do Enum
        :return: lista de tuplas (NAME, VALUE)
        """
        return [(n.name, n.value) for n in cls]