from django.conf.urls import include, url

from api.urls import (apresentacao, atualizacao, auth, bairro, banco, cidade,
                      cliente, estoque, farmacia, laboratorio, pedido, post,
                      principio_ativo, produto, representante_legal, secao,
                      tabela_preco, uf, regiao, notificacao, conta)
from api.views.financeiro import urls as financeiro_urls
from api.views.root import HomeApiView

urlpatterns = [
    url(r'^$', HomeApiView.as_view(), name='home-api'),

    url(r'^ultima_atualizacao/', include(atualizacao)),

    url(r'^auth/', include(auth)),

    # Contas
    url(r'^contas/', include(conta)),

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

    # Regiões
    url(r'^regioes/', include(regiao)),

    # Notificação
    url(r'^notificacoes/', include(notificacao)),
]
