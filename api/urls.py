# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views.medicamento import *
from api.views.laboratorio import *
from api.views.cidade import *
from api.views.farmacia import *
from api.views.principio_ativo import *
from api.views.apresentacao import *
from api.views.root import HomeApiView

urlpatterns = [
    # Raiz
    url(r'^$', HomeApiView.as_view(), name='home-api'),

    # Farmacias
    url(r'^farmacias/$', FarmaciaList.as_view(), name='farmacia-list'),

    # Cidades
    url(r'^cidades/$', CidadeList.as_view(), name='cidade-list'),

    # Medicamentos
    url(r'^medicamentos/$', MedicamentoList.as_view(), name='medicamento-list'),
    url(r'^medicamentos/(?P<id>[0-9]+)/$', MedicamentoRetrieve.as_view(), name='medicamento-view'),

    # Apresetação
    url(r'^apresentacoes/(?P<id>[0-9]+)/$', ApresentacaoRetrieve.as_view(), name='apresentacao-view'),

    # Principios ativos
    url(r'^principios/$', PrincipioAtivoList.as_view(), name='principio-list'),

    # Laboratorios
    url(r'^laboratorios/$', LaboratorioList.as_view(), name='laboratorio-list'),

]
