from django.conf.urls import url

from api.views.principio_ativo import *


urlpatterns = [
    # Principios ativos
    url(r'^principios_ativos/$', PrincipioAtivoList.as_view(), name='principio_ativo-list'),
    url(r'^principios_ativos_export/$', PrincipioAtivoExport.as_view(), name='principio_ativo-export'),
    url(r'^principios_ativos/sync/(?P<data>[0-9]+)/$', PrincipioAtivoSync.as_view(), name='principio_ativo-sync'),
]
