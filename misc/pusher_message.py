from pusher import pusher


class Message(object):
    """
    Mensagem para enviar via pusher
    """
    def __init__(self, channel=None, event=None, data=None):
        """
        Construtor
        :param channel: Canal
        :param event: Evento
        :param data: Dicionario
        """
        self.channel = channel
        self.event = event
        self.data = data
        self.pusher_client = pusher.Pusher(
            app_id='290714',
            key='2e48b48ce3b0da0fa501',
            secret='c2580e52f54ccaf543ab',
            ssl=True
        )

    def send(self, channel=None, event=None, data=None):
        try:
            self.pusher_client.trigger(
                channel if channel else self.channel,
                event if event else self.event,
                data if data else self.data
            )
        except:
            pass
