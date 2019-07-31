from django.conf.urls import url

from api.views.banco import *

urlpatterns = [
    # Banco
    url(r'^$', BancoList.as_view(), name='banco-list'),
]
