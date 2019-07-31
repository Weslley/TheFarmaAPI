from django.conf.urls import url

from api.views.financeiro.base import (
    ResumoFinanceiro,
    MaisVendidosNaRegiao,
    ResumoListagemVendas,
    MedicamentosMaisVendidos,
    MedicamentosMaisVendidosDetalhes,
    MaisPesquisadoNoRaio
)

urlpatterns = [
    # Raiz
    url(r'^$', ResumoFinanceiro.as_view(), name='financeiro-api-view'),
    url(r'^vendas/', ResumoListagemVendas.as_view(), name='financeiro-sales-api-view'),
    url(r'^mais_vendido/$', MedicamentosMaisVendidos.as_view(), name='financeiro-more-saled-api-view'),
    url(r'^mais_vendido/(?P<id>[0-9]+)/$', MedicamentosMaisVendidosDetalhes.as_view(), name='financeiro-more-saled-api-detail'),
    url(r'^mais_vendidos_raio/$', MaisVendidosNaRegiao.as_view(), name='financeiro-more-saled-in-thunder'),
    url(r'^mais_pesquisado_raio/$', MaisPesquisadoNoRaio.as_view(), name='financeiro-more-search-in-thunder'),
]