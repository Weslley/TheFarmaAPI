from django.conf.urls import url

from api.views.regiao import *

urlpatterns = [
    # Regiões
    url(r'^$', RegiaoList.as_view(), name='principio_ativo-list'),
]
