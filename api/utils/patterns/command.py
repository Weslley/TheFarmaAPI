import sys, inspect
from api.utils import Converter


class CommandNotFound(Exception):
    """
    Exception para comando que não existe
    """
    pass


class CommandItem():
    """
    Classe que representa o comando a ser executado
    """

    _next = None

    def execute_command(self, context, **kwargs):
        pass

    def execute(self, context, **kwargs):
        self.execute_command(context, **kwargs)
        if self._next:
            self._next.execute(context, **kwargs)



class CommandPattern():
    """
    Classe para representar o padrão command
    """
    def __init__(self, *args, **kwargs):
        clsmembers = inspect.getmembers(sys.modules[kwargs['__name__']], inspect.isclass)
        clsmembers = [(Converter.snake_case(name)[:-8], command) \
            for name, command in clsmembers \
            if name.endswith('Command') and issubclass(command, CommandItem)\
        ]
        self.commads = {key: value() for (key, value) in clsmembers}


    def execute(self, command_name, **kwargs):
        """
        Metodo que executa o comando
        :param command_name: Nome do comando a ser executado
        """
        context = {
            'controler': self
        }

        if not self.commads:
            raise CommandNotFound()

        assert type(self.commads) == dict, (
            'Commands should be an dict.'
        )

        if command_name in self.commads:
            self.commads[command_name].execute(context, **kwargs)
        else:
            raise CommandNotFound()
