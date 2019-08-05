from django.conf.urls import url
from apiv2.views.pedido import PedidoCreateListView, PedidoRetriveView
from apiv2.views.produto import ListDosagensProdutoView

urlpatterns = [
    url(r'^pedido/$',PedidoCreateListView.as_view(),name="apiv2-list-create-pedido"),
    url(r'^produto/dosagens$',ListDosagensProdutoView.as_view(),name="apiv2-list-dosagens-produto"),
    url(r'^pedido/(?P<pk>[0-9]+)/$', PedidoRetriveView.as_view(),name='apiv2-pedido-retrive'),
]