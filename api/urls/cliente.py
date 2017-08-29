from django.conf.urls import url

from api.views.cliente import *

urlpatterns = [

    # Clientes - Enderecos - Cartões
    url(r'^$', ClienteList.as_view(), name='cliente-list'),
    url(r'^(?P<id>[0-9]+)/$', ClienteRetrieve.as_view(), name='cliente-view'),
    url(r'^(?P<id_cliente>[0-9]+)/enderecos/$', EnderecoCreate.as_view(), name='cliente-endereco-list-create'),
    url(r'^(?P<id_cliente>[0-9]+)/enderecos/(?P<id>[0-9]+)/$', EnderecoUpdateDelete.as_view(), name='cliente-endereco-update-delete'),
    url(r'^(?P<id_cliente>[0-9]+)/cartoes/$', CartaoCreate.as_view(), name='cliente-cartao-list-create'),
    url(r'^(?P<id_cliente>[0-9]+)/cartoes/(?P<id>[0-9]+)/$', CartaoUpdateDelete.as_view(), name='cliente-cartao-update-delete'),

]
