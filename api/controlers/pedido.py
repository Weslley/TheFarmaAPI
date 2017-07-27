from api.models.pedido import Pedido
from api.utils.patterns.command import CommandPattern, CommandItem, CommandNotFound


class UltimoPedidoCommand(CommandItem):

    def execute_command(self, context, **kwargs):
        print(self.__class__.__name__)
        print(context)
        print(kwargs)

class PrimeiroPedidoCommand(CommandItem):

    _next = UltimoPedidoCommand()

    def execute_command(self, context, **kwargs):
        print(self.__class__.__name__)
        print(context)
        print(kwargs)


class PedidoControler(CommandPattern):
    """
    Classe responsavel pelas operações relacionadas ao pedido
    """
    def __init__(self, *args, **kwargs):
        kwargs['__name__'] = __name__
        super(PedidoControler, self).__init__(*args, **kwargs)

