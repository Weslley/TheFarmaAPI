from django.conf.urls import url

from api.views.produto import *


urlpatterns = [
    # Medicamentos
    url(r'^medicamentos/$', MedicamentoList.as_view(), name='medicamento-list'),
    url(r'^medicamentos/(?P<id>[0-9]+)/$', MedicamentoRetrieve.as_view(), name='medicamento-view'),
    url(r'^medicamentos_export/$', MedicamentoExport.as_view(), name='medicamento-export'),
    url(r'^medicamentos/sync/(?P<data>[0-9]+)/$', MedicamentoSync.as_view(), name='medicamento-sync'),

    # Produtos
    url(r'^produtos/(?P<uf>[A-Z]{2})/$', ProdutosBusca.as_view(), name='produto-list'),
]
