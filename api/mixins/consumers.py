import json
import re
from channels import Group
from rest_framework.authtoken.models import Token

from api.utils import methodize


def send(self, data, **kwargs):
    """
    Metodo para enviar mensagem para socket
    :param self: BaseConsumer
    :param data: Dicionario com dados a serem enviados
    :param kwargs: Valores extras nos cadosde groups com regex
    :return:
    """
    group = self.get_group(**kwargs) if kwargs else self.group if self.group else self.get_group(**kwargs)
    group.send({"text": json.dumps(data), })


class BaseConsumer(object):
    """
    Classe base para consumers dos channels
    """
    group = None
    group_name = None
    authenticated = False
    model = None
    url_kwarg = 'id'

    def __init__(self, message=None, data=None, **kwargs):

        if not self.group_name:
            raise Exception('group_name is None or empty string')

        if type(self.group_name) != str:
            raise Exception('group_name should be a str type')

        self.send = methodize(send, self)
        self.message = message
        self.data = data
        for key in kwargs.keys():
            if key != 'skip_group':
                setattr(self, key, kwargs[key])

        extra_keys = getattr(self, 'extra_keys', {})

        if ('skip_group' not in kwargs) or ('skip_group' in kwargs and not kwargs['skip_group']):
            self.group = self.get_group(**extra_keys)

    @classmethod
    def connect(cls, message,  *args, **kwargs):
        cls.validate_kwargs(kwargs)
        if cls.authenticated:
            if 'query_string' not in message.content:
                raise Exception('Authorization not in query string')

            query = message.content['query_string']
            key, value = query.decode('utf8').replace("'", '"').replace("%20", " ").split(':')
            try:
                Token.objects.get(key=value.split(' ')[1])
            except Token.DoesNotExist:
                raise Exception('Token inválido')

        kwargs = {'extra_keys': kwargs} if kwargs else {}
        instance = cls(message, **kwargs)
        message.reply_channel.send({"accept": True})
        instance.group.add(message.reply_channel)

    @classmethod
    def disconect(cls, message,  *args, **kwargs):
        kwargs = {'extra_keys': kwargs} if kwargs else {}
        instance = cls(message, **kwargs)
        instance.group.discard(message.reply_channel)

    @classmethod
    def receive(cls, message, *args, **kwargs):
        kwargs = {'extra_keys': kwargs} if kwargs else {}
        instance = cls(message, **kwargs)
        instance.dispatch()

    @classmethod
    def validate_kwargs(cls, data):
        if cls.model:
            if cls.url_kwarg in data:
                data = {cls.url_kwarg: data[cls.url_kwarg]}
                try:
                    cls.model.objects.get(**data)
                except cls.model.DoesNotExist:
                    raise Exception('Objeto {} não existe'.format(cls.model.__name__))
            else:
                raise Exception('Missing {} in url connect'.format(cls.url_kwarg))

    @classmethod
    def send(cls, data, **kwargs):
        cls(skip_group=True).send(data, **kwargs)

    def dispatch(self):
        raise NotImplementedError()

    def get_group(self, **kwargs):
        regex = r"{[a-zA-Z]+}"
        regex = re.compile(regex)
        matches = [re.sub(r"\W+", '', _).strip() for _ in regex.findall(self.group_name)]

        # veridicando se foi encontrado os formats
        if matches:
            # verificando se existem os itens referentes aos matchs
            if not all(_ in kwargs.keys() for _ in matches):
                raise Exception('Missing values in format, check kwargs')

            # verificando chaves duplicadas em group_name
            if not all(len([_ for _ in matches if _ == item]) == 1 for item in matches):
                raise Exception('Multiple values in format, check group_name')

            # limpando dicionario
            formats = {key: kwargs[key] for key in matches}

            return Group(self.group_name.format(**formats))

        return Group(self.group_name) if not self.group else self.group
