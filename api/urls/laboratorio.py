from django.conf.urls import url

from api.views.laboratorio import *


urlpatterns = [
    # Laboratorios
    url(r'^laboratorios/$', LaboratorioList.as_view(), name='laboratorio-list'),
    url(r'^laboratorios_export/$', LaboratorioExport.as_view(), name='laboratorio-export'),
    url(r'^laboratorios/sync/(?P<data>[0-9]+)/$', LaboratorioSync.as_view(), name='laboratorio-sync'),
]
