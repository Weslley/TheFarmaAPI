# -*- coding: utf-8 -*-

from django.conf.urls import url
from core.views.base import *
from core.views.posts import *
from core.views.produto import *
from core.views.usuarios import *
from core.views.parceiro import *
from core.views.atualizacao import *
from core.views.estoque import *
from core.views.farmacia import *
from core.views.bairro import *
from core.views.uf import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^desativar_usuario/(?P<id>[0-9]+)/(?P<fk_id>[0-9]+)/(?P<model>[a-z]+)/$', desativa_usuario, name='desativar-usuario'),
    # Post
    url(r'^posts/$', PostList.as_view(), name='post-admin-list'),
    url(r'^posts/adicionar/$', PostCreate.as_view(), name='post-admin-add'),
    url(r'^posts/(?P<id>[0-9]+)/$', PostDetail.as_view(), name='post-admin-view'),
    url(r'^posts/(?P<id>[0-9]+)/editar/$', PostUpdate.as_view(), name='post-admin-update'),
    url(r'^posts/(?P<id>[0-9]+)/remover/$', PostDelete.as_view(), name='post-admin-delete'),

    # Instituição
    url(r'^parceiros/$', ParceiroList.as_view(), name='parceiro-admin-list'),
    url(r'^parceiros/adicionar/$', ParceiroCreate.as_view(), name='parceiro-admin-add'),
    url(r'^parceiros/(?P<id>[0-9]+)/$', ParceiroDetail.as_view(), name='parceiro-admin-view'),
    url(r'^parceiros/(?P<id>[0-9]+)/adicionar/usuario/$', UsuarioParceiroCreate.as_view(), name='parceiro-admin-add-usuario'),

    # Medicamentos
    url(r'^produtos/$', MedicamentoList.as_view(), name='produto-admin-list'),
    url(r'^produtos/adicionar/$', MedicamentoCreate.as_view(), name='produto-admin-add'),
    url(r'^produtos/(?P<id>[0-9]+)/$', MedicamentoDetail.as_view(), name='produto-admin-view'),
    url(r'^produtos/(?P<id>[0-9]+)/editar/$', MedicamentoUpdate.as_view(), name='produto-admin-update'),
    url(r'^produtos/(?P<id>[0-9]+)/remover/$', MedicamentoDelete.as_view(), name='produto-admin-delete'),

    # Usuario
    url(r'^perfil/(?P<id>[0-9]+)/$', PerfilView.as_view(), name='perfil-view'),

    # Usuario
    url(r'^atualizacoes/$', AtualizacaoList.as_view(), name='atualizacao-admin-list'),
    url(r'^atualizacoes/adicionar/$', AtualizacaoCreate.as_view(), name='atualizacao-admin-add'),

    # Estoque
    url(r'^estoques/$', EstoqueList.as_view(), name='estoque-admin-list'),

    # Farmacia
    url(r'^farmacias/$', FarmaciaList.as_view(), name='farmacia-admin-list'),
    url(r'^farmacias/adicionar/$', FarmaciaCreate.as_view(), name='farmacia-admin-add'),
    url(r'^farmacias/(?P<id>[0-9]+)/$', FarmaciaDetail.as_view(), name='farmacia-admin-view'),
    url(r'^farmacias/(?P<id>[0-9]+)/adicionar/representante/$', RepresentanteCreate.as_view(), name='farmacia-admin-add-representante'),

    # Bairro
    # url(r'^bairros/$', busca_bairro_cidade, name='bairro-admin-list'),
    url(r'^bairros/busca/$', busca_bairro_cidade, name='bairro-admin-busca'),

    # Ufs
    url(r'^ufs/$', UfList.as_view(), name='uf-admin-list'),
    url(r'^ufs/adicionar/$', UfCreate.as_view(), name='uf-admin-add'),
    url(r'^ufs/(?P<id>[0-9]+)/$', UfUpdate.as_view(), name='uf-admin-view'),
]
