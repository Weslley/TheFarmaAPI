# -*- coding: utf-8 -*-
from pyrebase import pyrebase
from django.conf import settings
from rest_framework import status, generics
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import OrderingFilter, ApresentacaoFilter
from api.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from api.mixins.base import SyncApiMixin
from api.models.cidade import Cidade
from api.models.produto import Produto
from api.models.apresentacao import Apresentacao
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


class RankingApresentacao(APIView):
    """
    View para adicionar visualização à apresentação e ao medicamento
    """
    def post(self, request, id, format=None):
        return Response({'detail': 'sucesso'}, status=status.HTTP_200_OK)


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
    filter_class = ApresentacaoFilter
    ordering_fields = ('produto__nome', '-produto__nome')
    ordering = ('produto__nome',)

    def get_serializer_context(self):
        context = super(ApresentacaoPorEstadoList, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context


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

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context
