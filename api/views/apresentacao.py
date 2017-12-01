
from django.conf import settings
from django.db import transaction
from django.db.models import Sum, FloatField, F, Count, Value
# from django_filters.rest_framework import DjangoFilterBackend
from pyrebase import pyrebase
from rest_framework import generics, status
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import ApresentacaoFilter, OrderingFilter, ApresentacaoBuscaFilter
from api.mixins.base import SyncApiMixin
from api.models.apresentacao import Apresentacao
from api.models.cidade import Cidade
from api.models.configuracao import Configuracao
from api.models.produto import Produto
from api.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from api.serializers.apresentacao import *


class ApresentacaoRetrieve(generics.RetrieveAPIView):
    """
    View para o get da apresentação
    """
    lookup_url_kwarg = 'id'
    serializer_class = ApresentacaoSerializer

    def get_queryset(self):
        if 'id' in self.kwargs and self.kwargs['id']:
            return Apresentacao.objects.filter(id=self.kwargs['id'])
        else:
            return Apresentacao.objects.none()


class ApresentacaoList(generics.ListAPIView):
    """
    Listagem de apresentações
    """
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoListSerializer
    pagination_class = SmallResultsSetPagination


class ApresentacaoSync(generics.ListAPIView, SyncApiMixin):
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoExportSerializer
    pagination_class = LargeResultsSetPagination


class ApresentacaoExport(generics.ListAPIView):
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoExportSerializer
    pagination_class = LargeResultsSetPagination


class ApresentacaoPorEstadoList(generics.ListAPIView):
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoBuscaProduto
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ApresentacaoBuscaFilter

    def get_serializer_context(self):
        context = super(ApresentacaoPorEstadoList, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        cidades = Cidade.objects.filter(uf__sigla=unidade_federativa)

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = cidades.filter(nome__iexact=nome_cidade)

        if cidades.count():
            context['cidade'] = cidades.first()

        return context

    def get_queryset(self):
        qs = super(ApresentacaoPorEstadoList, self).get_queryset()
        c = Configuracao.objects.first()
        return qs.annotate(
            _ranking=Sum(F('ranking_visualizacao') * Value(c.peso_ranking_visualizacao), output_field=FloatField()) +
            Sum(F('ranking_proposta') * Value(c.peso_ranking_proposta), output_field=FloatField()) +
            Sum(F('ranking_compra') * Value(c.peso_ranking_compra), output_field=FloatField())
        ).order_by('patrocinio', '-_ranking')


class ApresentacaoMaisVendidasPorEstadoList(generics.ListAPIView):
    queryset = Apresentacao.objects.annotate(quantidade_vendas=Count('itens_vendidos__pedido__id', distinct=True))
    serializer_class = ApresentacaoBuscaProduto
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ApresentacaoFilter
    ordering_fields = ('quantidade_vendas', 'data_atualizacao')
    ordering = ('-quantidade_vendas', '-data_atualizacao')

    def get_serializer_context(self):
        context = super(ApresentacaoMaisVendidasPorEstadoList, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context


class ApresentacaoPorEstadoRetrieve(generics.RetrieveAPIView):
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoProdutoRetrieve
    lookup_url_kwarg = 'id'

    def get_serializer_context(self):
        context = super(ApresentacaoPorEstadoRetrieve, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context


class GenericosPorEstadoList(generics.ListAPIView):
    serializer_class = ApresentacaoBuscaProduto
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ApresentacaoFilter
    ordering_fields = ('produto__nome', '-produto__nome')
    ordering = ('produto__nome',)

    def get_queryset(self):
        produto = Produto.objects.get(apresentacoes__id=self.kwargs['id'])
        queryset = Apresentacao.objects.filter(produto__principio_ativo=produto.principio_ativo)
        return queryset

    def get_serializer_context(self):
        context = super(GenericosPorEstadoList, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        cidades = Cidade.objects.filter(uf__sigla=unidade_federativa)

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = cidades.filter(nome__iexact=nome_cidade)

        if cidades.count():
            context['cidade'] = cidades.first()

        return context


class RankingVisualizacaoUpdate(APIView):
    """
    View para adicionar visualização à apresentação e ao medicamento
    """
    def post(self, request, id, format=None):
        Apresentacao.objects.update_ranking_visualizacao(id)
        return Response({'detail': 'Sucesso'}, status=status.HTTP_200_OK)
