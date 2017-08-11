from django.conf.urls import url

from api.views.secao import *

urlpatterns = [
    # Seções
    url(r'^$', SecaoList.as_view(), name='secao-list'),
    url(r'^(?P<id>[0-9]+)/$', SecaoDetail.as_view(), name='secao-view'),
]
