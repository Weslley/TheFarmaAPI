from django.conf.urls import url

from api.views.farmacia import *

urlpatterns = [
    # Farmacias
    url(r'^$', FarmaciaList.as_view(), name='farmacia-list'),
]
