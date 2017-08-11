from django.conf.urls import url, include

from api.urls import (
    uf,
    auth,
    post,
    banco,
    secao,
    bairro,
    cidade,
    pedido,
    cliente,
    estoque,
    produto,
    farmacia,
    atualizacao,
    laboratorio,
    apresentacao,
    tabela_preco,
    principio_ativo,
    representante_legal
)

from api.views.root import HomeApiView
from api.views.financeiro import urls as financeiro_urls
from api.views.autenticacao import (
    Login,
    Logout,
    TesteLogin,
    LoginFacebook,
)

urlpatterns = [
    url(r'^ultima_atualizacao/', include(atualizacao)),

    # Login token
    url(r'^login/$', TesteLogin.as_view(), name='login'),
    url(r'^login_facebook/$', LoginFacebook.as_view(), name='login-facebook'),
    url(r'^login/cliente/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

    url(r'^auth/', include(auth)),


    # Farmacias
    url(r'^farmacias/', include(farmacia)),

    # Cidades
    url(r'^cidades/', include(cidade)),

    # Bairros
    url(r'^bairros/', include(bairro)),

    # Medicamentos
    url(r'^medicamentos/', include(produto)),

    # Produtos
    url(r'^produtos/', include(produto)),

    # Apresetação
    url(r'^apresentacoes/', include(apresentacao)),

    # Principios ativos
    url(r'^principios_ativos/', include(principio_ativo)),

    # Laboratorios
    url(r'^laboratorios/', include(laboratorio)),

    # Tabelas de preços
    url(r'^tabela_precos/', include(tabela_preco)),

    # UFs
    url(r'^ufs/', include(uf)),

    # Post
    url(r'^posts/', include(post)),

    # Estoque
    url(r'^estoques/', include(estoque)),

    # Clientes - Enderecos - Cartões
    url(r'^clientes/', include(cliente)),

    # Seções
    url(r'^secoes/', include(secao)),

    # Representantes legais
    url(r'^representante_legal/', include(representante_legal)),

    # Banco
    url(r'^bancos/', include(banco)),

    # Financeiro
    url(r'^financeiro/', include(financeiro_urls)),

    # Pedidos
    url(r'^pedidos/', include(pedido)),
]
