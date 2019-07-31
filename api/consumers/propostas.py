from api.mixins.consumers import BaseConsumer
from channels.security.websockets import allowed_hosts_only


class PropostasConsumer(BaseConsumer):
    group_name = 'propostas'

    def dispatch(self):
        # self.send({'mensagem': "[user] %s" % self.message.content['text']})
        print('Chegou')
