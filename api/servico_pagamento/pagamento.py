"""
Módulo responsável para gerenciar pagamentos
"""
import inspect
from api.servico_pagamento import servicos as _servicos
from api.servico_pagamento.servicos.servico_abc import Servico


class Pagamento:
    """
    Classe de pagamento
    """
    servicos = []
    modules = [module for name, module in inspect.getmembers(_servicos, inspect.ismodule) if name != 'servico_abc']
    for mod in modules:
        _servicos = [_class for name, _class in inspect.getmembers(mod, inspect.isclass) if Servico in _class.__bases__]
        servicos.extend(_servicos)

    @classmethod
    def pagar(cls, tipo_servico, data):
        """
        Método que realiza o pagamento baseado nos servico selecionado
        """

        try:
            servico = [_class for _class in cls.servicos if _class.tipo_servico() == tipo_servico][0]
            return servico.realizar_pagamento(data)
        except IndexError:
            raise ServicoNaoImplementado()

        return None


    @classmethod
    def cancelar(cls, tipo_servico, data):
        """
        Método que realiza o cancelamento baseado nos servico selecionado
        """

        try:
            servico = [_class for _class in cls.servicos if _class.tipo_servico() == tipo_servico][0]
            return servico.realizar_cancelamento(data)
        except IndexError:
            raise ServicoNaoImplementado()

        return None


class ServicoNaoImplementado(Exception):
    pass
