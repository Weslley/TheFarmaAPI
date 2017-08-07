from channels.routing import include

from api.routing.farmacia import routing as farma_routing

channels_routing = [
    # You can use a string import path as the first argument as well.
    include(farma_routing, path=r"^/farmacias"),
]