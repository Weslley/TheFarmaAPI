from channels.routing import include

from api.routing.farmacia import routing as farmacias
from api.routing.propostas import routing as propostas

channels_routing = [
    # You can use a string import path as the first argument as well.
    include(farmacias, path=r'^/farmacias/(?P<id>[0-9]+)/$'),
    include(propostas, path=r"^/propostas"),
]
