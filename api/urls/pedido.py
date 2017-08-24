from django.conf.urls import url

from api.views.pedido import PedidoCreate, PropostasList

urlpatterns = [
    # Pedidos
    url(r'^$', PedidoCreate.as_view()),
    url(r'^propostas/$', PropostasList.as_view()),
]
