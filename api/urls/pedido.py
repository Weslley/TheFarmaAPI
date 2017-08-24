from django.conf.urls import url

from api.views.pedido import PedidoCreate, PropostaList, PropostaRetrieveUpdate

urlpatterns = [
    # Pedidos
    url(r'^$', PedidoCreate.as_view()),
    url(r'^propostas/$', PropostaList.as_view()),
    url(r'^(?P<id>[0-9]+)/propostas/$', PropostaRetrieveUpdate.as_view()),
]
