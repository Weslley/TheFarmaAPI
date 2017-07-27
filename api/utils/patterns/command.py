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
    required_kwargs = None

    def assert_required_kwargs(self, **kwargs):
        if self.required_kwargs:
            assert all(key in kwargs for key in self.required_kwargs), (
                'Check for all required kwargs in execution. Missing {} kwargs'.format(
                    [key for key in self.required_kwargs if key not in  kwargs]
                )
            )


    def execute_command(self, context, **kwargs):
        pass

    def execute(self, context, **kwargs):
        self.assert_required_kwargs(**kwargs)
        self.execute_command(context, **kwargs)
        if self._next:
            self._next.execute(context, **kwargs)



class CommandPattern():
    """
    Classe para representar o padrão command
    """
    def __init__(self, *args, **kwargs):
        clsmembers = inspect.getmembers(sys.modules[self.__module__], inspect.isclass)
        clsmembers = [(Converter.snake_case(name)[:-8], command) \
            for name, command in clsmembers \
            if name.endswith('Command') and issubclass(command, CommandItem)\
        ]
        self._commads = {key: value() for (key, value) in clsmembers}


    def execute(self, command_name, **kwargs):
        """
        Metodo que executa o comando
        :param command_name: Nome do comando a ser executado
        """
        context = {
            'controler': self
        }

        if not self._commads:
            raise CommandNotFound()

        assert type(self._commads) == dict, (
            'Commands should be an dict.'
        )

        if command_name in self._commads:
            self._commads[command_name].execute(context, **kwargs)
        else:
            raise CommandNotFound()

    @property
    def commads(self):
        """
        :return: Lista do nome dos comandos
        """
        return list(self._commads.keys())
