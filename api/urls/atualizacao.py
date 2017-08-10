from django.conf.urls import url

from api.views.atualizacao import UltimaAtualizacao

urlpatterns = [
    url(r'^ultima_atualizacao/$', UltimaAtualizacao.as_view(), name='ultima-atualizacoa-api'),
]
