from django.conf.urls import url

from api.views.estoque import *


urlpatterns = [
    # Estoque
    url(r'^estoques/add/$', EstoqueCreateUpdate.as_view(), name='estoque-add'),
]
