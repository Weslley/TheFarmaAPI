# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.apresentacao import Apresentacao
from api.models.cidade import Cidade
from api.pagination import SmallResultsSetPagination, LargeResultsSetPagination
from api.serializers.apresentacao import *
from api.filters import ApresentacaoFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


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

