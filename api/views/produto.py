# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import MedicamentoFilter, OrderingFilter
from api.mixins.base import SyncApiMixin
from api.models.produto import Produto
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import SmallResultsSetPagination, StandardResultsSetPagination, LargeResultsSetPagination
from api.serializers.medicamento import *
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

