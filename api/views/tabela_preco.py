from pyrebase import pyrebase
from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from api.pagination import (
    LargeResultsSetPagination,
    SmallResultsSetPagination,
    ExtraLargeResultsSetPagination
)
from api.mixins.base import SyncApiMixin
from api.models.atualizacao import Atualizacao
from api.models.tabela_preco import TabelaPreco
from api.serializers.tabela_preco import TabelaPrecoSerializer


class TabelaPrecoList(generics.ListAPIView):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer
    pagination_class = LargeResultsSetPagination


class TabelaPrecoExport(generics.ListAPIView):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer
    pagination_class = LargeResultsSetPagination


class TabelaPrecoSync(generics.ListAPIView, SyncApiMixin):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer
    pagination_class = LargeResultsSetPagination
