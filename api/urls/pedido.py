from django.conf.urls import url

from api.views.pedido import PedidoCreate, PropostaList, PropostaRetrieveUpdate, PedidoRetrieve, PedidoCheckout, \
    PedidoCancelamentoCliente, UltimoPedido, PropostaCancelamentoFarmacia

urlpatterns = [
    # Pedidos
    url(r'^$', PedidoCreate.as_view()),
    url(r'^(?P<id>[0-9]+)/$', PedidoRetrieve.as_view()),
    url(r'^ultimo/$', UltimoPedido.as_view()),
    url(r'^propostas/$', PropostaList.as_view()),
    url(r'^(?P<id>[0-9]+)/propostas/$', PropostaRetrieveUpdate.as_view()),
    url(r'^(?P<id>[0-9]+)/checkout/$', PedidoCheckout.as_view()),
    url(r'^(?P<id>[0-9]+)/cancelamento_cliente/$', PedidoCancelamentoCliente.as_view()),
    url(r'^(?P<id>[0-9]+)/cancelamento_proposta/$', PropostaCancelamentoFarmacia.as_view()),
]
