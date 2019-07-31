from channels.routing import route

from api.consumers.propostas import *

routing = [
    route('websocket.connect', PropostasConsumer.connect),
    route('websocket.receive', PropostasConsumer.receive),
    route('websocket.disconnect', PropostasConsumer.disconect),
]
