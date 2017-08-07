from channels.routing import route
from api.consumers.farmacia import *


routing = [
    route('websocket.connect', FarmaciaConsumer.connect),
    route('websocket.receive', FarmaciaConsumer.receive),
    route('websocket.disconnect', FarmaciaConsumer.disconect),
]
