from django.conf.urls import include, url

from api.views.financeiro import urls as financeiro_urls

urlpatterns = [
    # Financeiro
    url(r'^financeiro/', include(financeiro_urls)),
]
