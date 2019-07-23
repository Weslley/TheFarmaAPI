from django.conf.urls import url
from apiv2.views.pedido import PedidoCreateListView
from apiv2.views.produto import ListDosagensProdutoView

urlpatterns = [
    url(r'^pedido/$',PedidoCreateListView.as_view(),name="apiv2-list-create-pedido"),
    url(r'^produto/(?P<nome>[a-z]+)/dosagens$',ListDosagensProdutoView.as_view(),name="apiv2-list-dosagens-produto")
]