from django.conf.urls import url, include

from api.views.financeiro import urls as financeiro_urls

urlpatterns = [
    # Financeiro
    url(r'^financeiro/', include(financeiro_urls)),
]
