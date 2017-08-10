from django.conf.urls import url

from api.views.tabela_preco import *


urlpatterns = [
    # Tabelas de preços
    url(r'^tabela_precos/$', TabelaPrecoList.as_view(), name='tabela_preco-list'),
    url(r'^tabela_precos_export/$', TabelaPrecoExport.as_view(), name='tabela_preco-export'),
    url(r'^tabela_precos/sync/(?P<data>[0-9]+)/$', TabelaPrecoSync.as_view(), name='tabela_preco-sync'),
]
