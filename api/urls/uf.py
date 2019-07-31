from django.conf.urls import url

from api.views.uf import *

urlpatterns = [
    # UFs
    url(r'^$', UfList.as_view(), name='uf-list'),
    url(r'^ufs_export/$', UfExport.as_view(), name='uf-export'),
    url(r'^sync/(?P<data>[0-9]+)/$', UfSync.as_view(), name='uf-sync'),
]
