import json

from channels import Group


class BaseConsumer(object):
    """
    Classe base para consumers dos channels
    """
    group_name = None

    def __init__(self, message=None, data=None, **kwargs):

        assert self.group_name, 'group_name is None or empty string'

        assert type(self.group_name) == str, 'group_name should be a str type'

        self.group = Group(self.group_name)
        self.message = message
        self.data = data
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    @classmethod
    def connect(cls, message):
        instance = cls(message)
        message.reply_channel.send({"accept": True})
        instance.group.add(message.reply_channel)

    @classmethod
    def disconect(cls, message):
        instance = cls(message)
        instance.group.discard(message.reply_channel)

    @classmethod
    def receive(cls, message):
        instance = cls(message)
        instance.dispatch()

    def dispatch(self):
        raise NotImplementedError()

    def send(self, data):
        self.group.send({"text": json.dumps(data), })
