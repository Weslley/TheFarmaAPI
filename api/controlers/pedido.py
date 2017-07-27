from api.models.pedido import Pedido
from api.utils.patterns.command import CommandPattern, CommandItem, CommandNotFound


class PedidoControler(CommandPattern):
    """
    Classe responsavel pelas operações relacionadas ao pedido
    """

    pass


class GetOrCreateCommand(CommandItem):

    required_kwargs = ['teste', ]

    def execute_command(self, context, **kwargs):
        print('Execucao')
