"""
Classe para ser herdada nos outros servicos
"""
from abc import abstractmethod, ABC


class Servico(ABC):

    @classmethod
    @abstractmethod
    def realizar_pagamento(cls, data):
        """Metodo para realizar o pagamento"""


    @classmethod
    @abstractmethod
    def realizar_cancelamento(cls, data):
        """Metodo para realizar o cancelamento"""

    @classmethod
    def tipo_servico(cls):
        return None
