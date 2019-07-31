from django.conf.urls import url

from api.views.principio_ativo import *

urlpatterns = [
    # Principios ativos
    url(r'^$', PrincipioAtivoList.as_view(), name='principio_ativo-list'),
    url(r'^(?P<pk>[0-9]+)/$', PrincipioAtivoRetrieve.as_view(), name='principio_ativo-retrieve'),
    url(r'^principios_ativos_export/$', PrincipioAtivoExport.as_view(), name='principio_ativo-export'),
    url(r'^sync/(?P<data>[0-9]+)/$', PrincipioAtivoSync.as_view(), name='principio_ativo-sync'),
]
