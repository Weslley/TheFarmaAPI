from django.conf.urls import url

from api.views.laboratorio import *

urlpatterns = [
    # Laboratorios
    url(r'^$', LaboratorioList.as_view(), name='laboratorio-list'),
    url(r'^(?P<pk>[0-9]+)/$', LaboratorioRetrieve.as_view(), name='laboratorio-retrieve'),
    url(r'^laboratorios_export/$', LaboratorioExport.as_view(), name='laboratorio-export'),
    url(r'^sync/(?P<data>[0-9]+)/$', LaboratorioSync.as_view(), name='laboratorio-sync'),
]
