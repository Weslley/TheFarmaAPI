"""
Classe para ser herdada nos outros servicos
"""
from abc import abstractmethod, ABC


class Servico(ABC):

    @classmethod
    @abstractmethod
    def realizar_pagamento(cls, **kwargs):
        """Metodo para realizar o pagamento"""

    @classmethod
    def tipo_servico(cls):
        return None