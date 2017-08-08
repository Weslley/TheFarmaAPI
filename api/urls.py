# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from api.views.atualizacao import UltimaAtualizacao
from api.views.bairro import *
from api.views.banco import *
from api.views.cliente import *
from api.views.produto import *
from api.views.laboratorio import *
from api.views.cidade import *
from api.views.farmacia import *
from api.views.post import *
from api.views.principio_ativo import *
from api.views.apresentacao import *
from api.views.root import HomeApiView
from api.views.secao import *
from api.views.tabela_preco import *
from api.views.estoque import *
from api.views.uf import *
from api.views.representante_legal import *
from api.views.autenticacao import Logout, LoginFacebook, TesteLogin, LoginFarmacia, Login, LoginDefault, CreateUser
from api.views.financeiro import urls as financeiro_urls


urlpatterns = [
    # Raiz
    url(r'^$', HomeApiView.as_view(), name='home-api'),
    url(r'^ultima_atualizacao/$', UltimaAtualizacao.as_view(), name='ultima-atualizacoa-api'),

    # Login token
    url(r'^login/$', TesteLogin.as_view(), name='login'),
    url(r'^login_facebook/$', LoginFacebook.as_view(), name='login-facebook'),
    url(r'^login/cliente/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^auth/logout/$', Logout.as_view(), name='logout'),
    url(r'^auth/users/$', CreateUser.as_view(), name='create-user'),
    url(r'^auth/login/$', LoginDefault.as_view(), name='login-user'),
    url(r'^auth/farmacia/login/$', LoginFarmacia.as_view(), name='login-farmacia'),


    # Farmacias
    url(r'^farmacias/$', FarmaciaList.as_view(), name='farmacia-list'),
    url(r'^envia_pedidos/$', FarmaciaPedidos.as_view(), name='farmacia-list-pedidos'),

    # Cidades
    url(r'^cidades/$', CidadeList.as_view(), name='cidade-list'),
    url(r'^cidades/(?P<ibge>[0-9]+)/$', CidadeDetail.as_view(), name='cidade-view'),

    # Bairros
    url(r'^bairros/(?P<ibge>[0-9]+)/$', BairroList.as_view(), name='bairro-list'),

    # Medicamentos
    url(r'^medicamentos/$', MedicamentoList.as_view(), name='medicamento-list'),
    url(r'^medicamentos/(?P<id>[0-9]+)/$', MedicamentoRetrieve.as_view(), name='medicamento-view'),
    url(r'^medicamentos_export/$', MedicamentoExport.as_view(), name='medicamento-export'),
    url(r'^medicamentos/sync/(?P<data>[0-9]+)/$', MedicamentoSync.as_view(), name='medicamento-sync'),

    # Produtos
    url(r'^produtos/(?P<uf>[A-Z]{2})/$', ProdutosBusca.as_view(), name='produto-list'),

    # Apresetação
    url(r'^apresentacoes/(?P<id>[0-9]+)/$', ApresentacaoRetrieve.as_view(), name='apresentacao-view'),
    url(r'^apresentacoes/$', ApresentacaoList.as_view(), name='apresentacao-list'),
    url(r'^apresentacoes_export/$', ApresentacaoExport.as_view(), name='apresentacao-export'),
    url(r'^apresentacoes/(?P<id>[0-9]+)/rank/$', RankingApresentacao.as_view(), name='apresentacao-ranking'),
    url(r'^apresentacoes/sync/(?P<data>[0-9]+)/$', ApresentacaoSync.as_view(), name='apresentacao-sync'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/$', ApresentacaoPorEstadoList.as_view(), name='apresentacao-list-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/mais_vendidos/$', ApresentacaoMaisVendidasPorEstadoList.as_view(), name='apresentacao-mais-vendida-list-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/(?P<id>[0-9]+)/$', ApresentacaoPorEstadoRetrieve.as_view(), name='apresentacao-retrieve-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/(?P<id>[0-9]+)/genericos/$', GenericosPorEstadoList.as_view(), name='apresentacao-genericos'),

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

    # UFs
    url(r'^ufs/$', UfList.as_view(), name='uf-list'),
    url(r'^ufs_export/$', UfExport.as_view(), name='uf-export'),
    url(r'^ufs/sync/(?P<data>[0-9]+)/$', UfSync.as_view(), name='uf-sync'),

    # Post
    url(r'^posts/$', PostExportList.as_view(), name='post-list'),
    url(r'^posts/(?P<id>[0-9]+)/like/$', CurtirView.as_view(), name='post-like'),
    url(r'^posts/likes/$', PostsCurtidosView.as_view(), name='like-list'),

    # Estoque
    url(r'^estoques/add/$', EstoqueCreateUpdate.as_view(), name='estoque-add'),

    # Clientes - Enderecos - Cartões
    url(r'^clientes/$', ClienteCreate.as_view(), name='cliente-create'),
    url(r'^clientes/enderecos/$', EnderecoCreate.as_view(), name='cliente-endereco-list-create'),
    url(r'^clientes/enderecos/(?P<id>[0-9]+)/$', EnderecoUpdateDelete.as_view(), name='cliente-endereco-update-delete'),
    url(r'^clientes/cartoes/$', CartaoCreate.as_view(), name='cliente-cartao-list-create'),
    url(r'^clientes/cartoes/(?P<id>[0-9]+)/$', CartaoUpdateDelete.as_view(), name='cliente-cartao-update-delete'),

    # Seções
    url(r'^secoes/$', SecaoList.as_view(), name='secao-list'),
    url(r'^secoes/(?P<id>[0-9]+)/$', SecaoDetail.as_view(), name='secao-view'),

    # Representantes legais
    url(r'^representante_legal/$', RepresentanteRetrieve.as_view(), name='representante-view'),

    # Banco
    url(r'^bancos/$', BancoList.as_view(), name='banco-list'),

    # Financeiro
    url(r'^financeiro/', include(financeiro_urls)),
]
