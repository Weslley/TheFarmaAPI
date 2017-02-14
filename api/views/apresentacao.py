# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.apresentacao import Apresentacao
from api.pagination import SmallResultsSetPagination, LargeResultsSetPagination
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
