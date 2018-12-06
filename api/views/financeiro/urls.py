from django.conf.urls import url

from api.views.financeiro.base import ResumoFinanceiro, ResumoListagemVendas

urlpatterns = [
    # Raiz
    url(r'^$', ResumoFinanceiro.as_view(), name='financeiro-api-view'),
    url(r'^vendas/', ResumoListagemVendas.as_view(), name='financeiro-sales-api-view'),
]
