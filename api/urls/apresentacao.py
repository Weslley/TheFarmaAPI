from django.conf.urls import url
from api.views.apresentacao import *


urlpatterns = [
    url(r'^apresentacoes/(?P<id>[0-9]+)/$', ApresentacaoRetrieve.as_view(), name='apresentacao-view'),
    url(r'^apresentacoes/$', ApresentacaoList.as_view(), name='apresentacao-list'),
    url(r'^apresentacoes_export/$', ApresentacaoExport.as_view(), name='apresentacao-export'),
    url(r'^apresentacoes/(?P<id>[0-9]+)/rank/$', RankingApresentacao.as_view(), name='apresentacao-ranking'),
    url(r'^apresentacoes/sync/(?P<data>[0-9]+)/$', ApresentacaoSync.as_view(), name='apresentacao-sync'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/$', ApresentacaoPorEstadoList.as_view(), name='apresentacao-list-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/mais_vendidos/$', ApresentacaoMaisVendidasPorEstadoList.as_view(), name='apresentacao-mais-vendida-list-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/(?P<id>[0-9]+)/$', ApresentacaoPorEstadoRetrieve.as_view(), name='apresentacao-retrieve-estado'),
    url(r'^apresentacoes/(?P<uf>[A-Z]{2})/(?P<id>[0-9]+)/genericos/$', GenericosPorEstadoList.as_view(), name='apresentacao-genericos'),
]
