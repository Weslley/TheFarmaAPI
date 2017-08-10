from django.conf.urls import url

from api.views.representante_legal import *

urlpatterns = [
    # Representantes legais
    url(r'^representante_legal/$', RepresentanteRetrieve.as_view(), name='representante-view'),
]
