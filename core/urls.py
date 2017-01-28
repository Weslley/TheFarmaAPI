# -*- coding: utf-8 -*-

from django.conf.urls import url
from core.views.base import *
from core.views.posts import *
from core.views.medicamentos import *
from core.views.usuarios import *
from core.views.instituicoes import *
from core.views.atualizacao import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    # Post
    url(r'^posts/$', PostList.as_view(), name='post-admin-list'),
    url(r'^posts/adicionar/$', PostCreate.as_view(), name='post-admin-add'),
    url(r'^posts/(?P<id>[0-9]+)/$', PostDetail.as_view(), name='post-admin-view'),

    # Instituição
    url(r'^instituicoes/$', InstituicaoList.as_view(), name='instituicao-admin-list'),
    url(r'^instituicoes/adicionar/$', InstituicaoCreate.as_view(), name='instituicao-admin-add'),
    url(r'^instituicoes/(?P<id>[0-9]+)/$', InstituicaoDetail.as_view(), name='instituicao-admin-view'),

    # Medicamentos
    url(r'^medicamentos/$', MedicamentoList.as_view(), name='medicamento-admin-list'),
    url(r'^medicamentos/adicionar/$', MedicamentoCreate.as_view(), name='medicamento-admin-add'),
    url(r'^medicamentos/(?P<id>[0-9]+)/$', MedicamentoDetail.as_view(), name='medicamento-admin-view'),
    url(r'^medicamentos/(?P<id>[0-9]+)/editar/$', MedicamentoUpdate.as_view(), name='medicamento-admin-update'),
    url(r'^medicamentos/(?P<id>[0-9]+)/remover/$', MedicamentoDelete.as_view(), name='medicamento-admin-delete'),

    # Usuario
    url(r'^perfil/(?P<id>[0-9]+)/$', PerfilView.as_view(), name='perfil-view'),

    # Usuario
    url(r'^atualizacoes/$', AtualizacaoList.as_view(), name='atualizacao-admin-list'),
    url(r'^atualizacoes/adicionar/$', AtualizacaoCreate.as_view(), name='atualizacao-admin-add'),


]
