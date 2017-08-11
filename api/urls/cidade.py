from django.conf.urls import url

from api.views.cidade import *

urlpatterns = [
    url(r'^$', CidadeList.as_view(), name='cidade-list'),
    url(r'^(?P<ibge>[0-9]+)/$', CidadeDetail.as_view(), name='cidade-view'),
]
