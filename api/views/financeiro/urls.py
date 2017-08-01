from django.conf.urls import url

from api.views.financeiro.base import ResumoFinanceiro

urlpatterns = [
    # Raiz
    url(r'^$', ResumoFinanceiro.as_view(), name='financeiro-api-view'),
]
