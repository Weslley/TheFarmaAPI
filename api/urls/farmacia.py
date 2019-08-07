from django.conf.urls import url

from api.views.farmacia import *

urlpatterns = [
    # Farmacias
    url(r'^$', FarmaciaList.as_view(), name='farmacia-list'),
    url(r'^(?P<id>[0-9]+)/$', FarmaciaRetrieve.as_view(), name='farmacia-retrieve'),
]
