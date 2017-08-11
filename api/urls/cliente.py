from django.conf.urls import url

from api.views.cliente import *

urlpatterns = [

    # Clientes - Enderecos - Cartões
    url(r'^$', ClienteCreate.as_view(), name='cliente-create'),
    url(r'^enderecos/$', EnderecoCreate.as_view(), name='cliente-endereco-list-create'),
    url(r'^enderecos/(?P<id>[0-9]+)/$', EnderecoUpdateDelete.as_view(), name='cliente-endereco-update-delete'),
    url(r'^cartoes/$', CartaoCreate.as_view(), name='cliente-cartao-list-create'),
    url(r'^cartoes/(?P<id>[0-9]+)/$', CartaoUpdateDelete.as_view(), name='cliente-cartao-update-delete'),

]
