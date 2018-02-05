from django.conf.urls import url

from api.views.produto import *

urlpatterns = [
    # Medicamentos
    url(r'^$', MedicamentoList.as_view(), name='medicamento-list'),
    url(r'^(?P<id>[0-9]+)/$', MedicamentoRetrieve.as_view(), name='medicamento-view'),
    url(r'^medicamentos_export/$', MedicamentoExport.as_view(), name='medicamento-export'),
    url(r'^sync/(?P<data>[0-9]+)/$', MedicamentoSync.as_view(), name='medicamento-sync'),

    # Produtos
    url(r'^(?P<uf>[A-Z]{2})/$', ProdutosBusca.as_view(), name='produto-list'),
    url(r'^v2/(?P<uf>[A-Z]{2})/$', ProdutosBuscaNova.as_view(), name='produto-list2'),
    url(r'^mais_vendidos/$', ProdutoIndicadorVenda.as_view(), name='indicador-produtos-mais-vendidos')
]
