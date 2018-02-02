# -*- coding: utf-8 -*-
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Case, When
from api.filters import MedicamentoFilter, OrderingFilter, ProdutoFilter, ProdutoIndicadorVendaFilter
from api.mixins.base import SyncApiMixin
from api.models.cidade import Cidade
from api.models.produto import Produto
from api.models.enums import StatusPedido, StatusProduto
from api.pagination import (LargeResultsSetPagination,
                            SmallResultsSetPagination,
                            StandardResultsSetPagination)
from api.serializers.produto import *
from django.db.models import Count
from api.utils import tipo_produto


class MedicamentoList(generics.ListAPIView):
    """
    Listagem dos medicamentos cadastrados
    """
    queryset = Produto.objects.exclude(tipo=tipo_produto.NAO_MEDICAMENTO)
    serializer_class = MedicamentoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = MedicamentoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)


class MedicamentoSync(generics.ListAPIView, SyncApiMixin):
    queryset = Produto.objects.exclude(tipo=tipo_produto.NAO_MEDICAMENTO)
    serializer_class = MedicamentoExportSerializer
    pagination_class = LargeResultsSetPagination


class MedicamentoRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        if 'id' in self.kwargs and self.kwargs['id']:
            return Produto.objects.filter(id=self.kwargs['id'])
        else:
            return Produto.objects.none()


class MedicamentoExport(generics.ListAPIView):
    queryset = Produto.objects.exclude(tipo=tipo_produto.NAO_MEDICAMENTO)
    serializer_class = MedicamentoExportSerializer
    pagination_class = LargeResultsSetPagination


class ProdutosBusca(generics.ListAPIView):
    """
    Listagem de todos os produtos
    """
    queryset = Produto.objects.filter(apresentacoes__isnull=False).distinct()
    serializer_class = ProdutoSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ProdutoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)

    def get_serializer_context(self):
        context = super(ProdutosBusca, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context


class ProdutosBuscaNova(generics.ListAPIView):
    """
    Listagem de todos os produtos
    """
    queryset = Produto.objects.filter(apresentacoes__isnull=False).distinct()
    serializer_class = ProdutoNovoSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ProdutoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)

    def get_serializer_context(self):
        context = super(ProdutosBuscaNova, self).get_serializer_context()
        context['cidade'] = None

        unidade_federativa = self.kwargs['uf']
        nome_cidade = self.request.GET.get('cidade')

        if nome_cidade:
            nome_cidade = nome_cidade.strip()
            cidades = Cidade.objects.filter(uf__sigla=unidade_federativa, nome__iexact=nome_cidade)
            if cidades.count():
                context['cidade'] = cidades.first()

        return context

    def get_queryset(self):
        qs = super(ProdutosBuscaNova, self).get_queryset()
        qs = qs.values('nome').annotate(dcount=Count('nome'))
        return qs


class ProdutoIndicadorVenda(generics.ListAPIView):
    """
    Listar os produtos mais vendidos 
    """
    queryset = Produto.objects.filter(
        status=StatusProduto.PUBLICADO.value,
        apresentacoes__isnull=False
    ).distinct().select_related(
        'principio_ativo', 'laboratorio'
    ).annotate(
        vendas=Count(
            Case(
                When(apresentacoes__itens_vendidos__pedido__status=StatusPedido.ENTREGUE.value, then=1)
            )
        )
    ).filter(vendas__gte=1).order_by('-vendas')
    serializer_class = ProdutoIndicadorVendaSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ProdutoIndicadorVendaFilter
    ordering_fields = ('vendas', '-vendas')
    ordering = ('-vendas',)
