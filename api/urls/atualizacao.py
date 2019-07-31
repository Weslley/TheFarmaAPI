from django.conf.urls import url

from api.views.atualizacao import UltimaAtualizacao

urlpatterns = [
    url(r'^$', UltimaAtualizacao.as_view(), name='ultima-atualizacoa-api'),
]
