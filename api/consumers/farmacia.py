from api.mixins.consumers import BaseConsumer


class FarmaciaConsumer(BaseConsumer):
    group_name = 'farmacias'

    def dispatch(self):
        self.send({'mensagem': "[user] %s" % self.message.content['text']})
