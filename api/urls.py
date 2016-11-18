# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views.bairro import BairroList
from api.views.medicamento import *
from api.views.laboratorio import *
from api.views.cidade import *
from api.views.farmacia import *
from api.views.post import *
from api.views.principio_ativo import *
from api.views.apresentacao import *
from api.views.root import HomeApiView
from api.views.tabela_preco import TabelaPrecoList
from api.views.user import Login, Logout

urlpatterns = [
    # Raiz
    url(r'^$', HomeApiView.as_view(), name='home-api'),

    # Login token
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

    # Farmacias
    url(r'^farmacias/$', FarmaciaList.as_view(), name='farmacia-list'),

    # Cidades
    url(r'^cidades/$', CidadeList.as_view(), name='cidade-list'),

    # Bairros
    url(r'^bairros/$', BairroList.as_view(), name='bairro-list'),

    # Medicamentos
    url(r'^medicamentos/$', MedicamentoList.as_view(), name='medicamento-list'),
    url(r'^medicamentos/(?P<id>[0-9]+)/$', MedicamentoRetrieve.as_view(), name='medicamento-view'),

    # Apresetação
    url(r'^apresentacoes/(?P<id>[0-9]+)/$', ApresentacaoRetrieve.as_view(), name='apresentacao-view'),
    url(r'^apresentacoes/$', ApresentacaoList.as_view(), name='apresentacao-list'),

    # Principios ativos
    url(r'^principios_ativos/$', PrincipioAtivoList.as_view(), name='principio_ativo-list'),

    # Laboratorios
    url(r'^laboratorios/$', LaboratorioList.as_view(), name='laboratorio-list'),

    # Tabelas de preços
    url(r'^tabela_precos/$', TabelaPrecoList.as_view(), name='tabela_preco-list'),

    # Post
    url(r'^posts/$', PostExportList.as_view(), name='post-list'),
    url(r'^posts/(?P<id>[0-9]+)/like/$', CurtirView.as_view(), name='post-list')

]
