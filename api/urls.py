# -*- coding: utf-8 -*-

from django.conf.urls import url

from api.views.atualizacao import UltimaAtualizacao
from api.views.bairro import BairroList
from api.views.medicamento import *
from api.views.laboratorio import *
from api.views.cidade import *
from api.views.farmacia import *
from api.views.post import *
from api.views.principio_ativo import *
from api.views.apresentacao import *
from api.views.root import HomeApiView
from api.views.tabela_preco import *
from api.views.user import Login, Logout, LoginFacebook, TesteLogin

urlpatterns = [
    # Raiz
    url(r'^$', HomeApiView.as_view(), name='home-api'),
    url(r'^ultima_atualizacao/$', UltimaAtualizacao.as_view(), name='ultima-atualizacoa-api'),

    # Login token
    url(r'^login/$', TesteLogin.as_view(), name='login'),
    url(r'^login_facebook/$', LoginFacebook.as_view(), name='login-facebook'),
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
    url(r'^medicamentos_export/$', MedicamentoExport.as_view(), name='medicamento-export'),
    url(r'^medicamentos/sync/(?P<data>[0-9]+)/$', MedicamentoSync.as_view(), name='medicamento-sync'),

    # Apresetação
    url(r'^apresentacoes/(?P<id>[0-9]+)/$', ApresentacaoRetrieve.as_view(), name='apresentacao-view'),
    url(r'^apresentacoes/$', ApresentacaoList.as_view(), name='apresentacao-list'),
    url(r'^apresentacoes_export/$', ApresentacaoExport.as_view(), name='apresentacao-export'),
    url(r'^apresentacoes/(?P<id>[0-9]+)/rank/$', RankingApresentacao.as_view(), name='apresentacao-ranking'),
    url(r'^apresentacoes/sync/(?P<data>[0-9]+)/$', ApresentacaoSync.as_view(), name='apresentacao-sync'),

    # Principios ativos
    url(r'^principios_ativos/$', PrincipioAtivoList.as_view(), name='principio_ativo-list'),
    url(r'^principios_ativos_export/$', PrincipioAtivoExport.as_view(), name='principio_ativo-export'),
    url(r'^principios_ativos/sync/(?P<data>[0-9]+)/$', PrincipioAtivoSync.as_view(), name='principio_ativo-sync'),

    # Laboratorios
    url(r'^laboratorios/$', LaboratorioList.as_view(), name='laboratorio-list'),
    url(r'^laboratorios_export/$', LaboratorioExport.as_view(), name='laboratorio-export'),
    url(r'^laboratorios/sync/(?P<data>[0-9]+)/$', LaboratorioSync.as_view(), name='laboratorio-sync'),

    # Tabelas de preços
    url(r'^tabela_precos/$', TabelaPrecoList.as_view(), name='tabela_preco-list'),
    url(r'^tabela_precos_export/$', TabelaPrecoExport.as_view(), name='tabela_preco-export'),
    url(r'^tabela_precos/sync/(?P<data>[0-9]+)/$', TabelaPrecoSync.as_view(), name='tabela_preco-sync'),

    # Post
    url(r'^posts/$', PostExportList.as_view(), name='post-list'),
    url(r'^posts/(?P<id>[0-9]+)/like/$', CurtirView.as_view(), name='post-list')

]
