# -*- coding: utf-8 -*-
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import MedicamentoFilter, OrderingFilter, ProdutoFilter
from api.mixins.base import SyncApiMixin
from api.models.cidade import Cidade
from api.models.produto import Produto
from api.pagination import (LargeResultsSetPagination,
                            SmallResultsSetPagination,
                            StandardResultsSetPagination)
from api.serializers.produto import *
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
