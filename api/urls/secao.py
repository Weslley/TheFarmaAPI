from django.conf.urls import url

from api.views.secao import *


urlpatterns = [
    # Seções
    url(r'^secoes/$', SecaoList.as_view(), name='secao-list'),
    url(r'^secoes/(?P<id>[0-9]+)/$', SecaoDetail.as_view(), name='secao-view'),
]
