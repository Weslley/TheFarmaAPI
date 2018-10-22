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
from datetime import datetime


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
    serializer_class = ProdutoIndicadorVendaSerializer

    def get_queryset(self):

        filter_kwargs = {
            'status': StatusProduto.PUBLICADO.value,
            'apresentacoes__isnull':False
        }

        ff = '%Y-%m-%d'
        data_inicial = self.request.GET.get('data_inicial', None)
        if data_inicial:
            filter_kwargs['apresentacoes__itens_vendidos__pedido__log__data_criacao__gte'] = datetime.strptime(data_inicial, ff)

        data_final = self.request.GET.get('data_final', None)
        if data_final:
            filter_kwargs['apresentacoes__itens_vendidos__pedido__log__data_criacao__lte'] = datetime.strptime(data_final, ff)

        laboratorio = self.request.GET.get('laboratorio', None)
        if laboratorio:
            filter_kwargs['laboratorio_id'] = laboratorio

        principio_ativo = self.request.GET.get('principio_ativo', None)
        if principio_ativo:
            filter_kwargs['principio_ativo_id'] = principio_ativo   

        regiao = self.request.GET.get('regiao', None)
        if regiao:
            filter_kwargs['apresentacoes__itens_vendidos__pedido__bairro__regiao_id'] = regiao   

        select_rel = ['principio_ativo', 'laboratorio']
        vendas_annotate = Count(
            Case(
                When(apresentacoes__itens_vendidos__pedido__status=StatusPedido.ENTREGUE.value, then=1)
            )
        )

        return Produto.objects.filter(
            **filter_kwargs
        ).select_related(
            *select_rel
        ).annotate(
            vendas=vendas_annotate
        ).filter(
            vendas__gte=1
        ).distinct().order_by('-vendas')