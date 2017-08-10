from django.conf.urls import url

from api.views.uf import *


urlpatterns = [
    # UFs
    url(r'^ufs/$', UfList.as_view(), name='uf-list'),
    url(r'^ufs_export/$', UfExport.as_view(), name='uf-export'),
    url(r'^ufs/sync/(?P<data>[0-9]+)/$', UfSync.as_view(), name='uf-sync'),
]
