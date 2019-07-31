from api.models.pedido import Pedido
from api.utils.patterns.command import CommandItem, CommandPattern


class PedidoControler(CommandPattern):
    """
    Classe responsavel pelas operações relacionadas ao pedido
    """

    model = Pedido


class GetOrCreateCommand(CommandItem):

    required_kwargs = ['cliente', '']

    def execute_command(self, context, **kwargs):
        print('Execucao')
