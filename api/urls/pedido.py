from django.conf.urls import url

from api.views.pedido import PedidoCreate

urlpatterns = [
    # Pedidos
    url(r'^$', PedidoCreate.as_view()),
]
