from django.conf.urls import url

from api.views.farmacia import *



urlpatterns = [
    # Farmacias
    url(r'^farmacias/$', FarmaciaList.as_view(), name='farmacia-list'),
    url(r'^envia_pedidos/$', FarmaciaPedidos.as_view(), name='farmacia-list-pedidos'),
]
