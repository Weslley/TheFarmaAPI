from django.conf.urls import url
from apiv2.views.pedido import PedidoCreateListView

urlpatterns = [
    url(r'^pedido/$',PedidoCreateListView.as_view(),name="apiv2-list-create-pedido"),
]