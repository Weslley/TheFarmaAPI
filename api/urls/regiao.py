from django.conf.urls import url

from api.views.regiao import *

urlpatterns = [
    # Regiões
    url(r'^$', RegiaoList.as_view(), name='regiao-list'),
    url(r'^(?P<pk>[0-9]+)/$', RegiaoRetrieve.as_view(), name='regiao-retrieve'),
]
