from django.conf.urls import url

from api.views.representante_legal import *

urlpatterns = [
    # Representantes legais
    url(r'^$', RepresentanteRetrieve.as_view(), name='representante-view'),
    url(r'^(?P<pk>[0-9]+)/$', RepresentanteFarmaciaView.as_view(), name='representantebyid-view'),
]
