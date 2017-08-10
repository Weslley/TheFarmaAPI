from django.conf.urls import url

from api.views.bairro import *


urlpatterns = [
    url(r'^bairros/(?P<ibge>[0-9]+)/$', BairroList.as_view(), name='bairro-list'),
]
