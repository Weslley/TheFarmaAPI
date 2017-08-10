from django.conf.urls import url

from api.views.cliente import *


urlpatterns = [

    # Clientes - Enderecos - Cartões
    url(r'^clientes/$', ClienteCreate.as_view(), name='cliente-create'),
    url(r'^clientes/enderecos/$', EnderecoCreate.as_view(), name='cliente-endereco-list-create'),
    url(r'^clientes/enderecos/(?P<id>[0-9]+)/$', EnderecoUpdateDelete.as_view(), name='cliente-endereco-update-delete'),
    url(r'^clientes/cartoes/$', CartaoCreate.as_view(), name='cliente-cartao-list-create'),
    url(r'^clientes/cartoes/(?P<id>[0-9]+)/$', CartaoUpdateDelete.as_view(), name='cliente-cartao-update-delete'),

]
