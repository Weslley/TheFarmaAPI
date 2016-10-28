# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.apresentacao import Apresentacao
from api.pagination import SmallResultsSetPagination
from api.serializers.apresentacao import *


class ApresentacaoRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = ApresentacaoSerializer

    def get_queryset(self):
        if 'id' in self.kwargs and self.kwargs['id']:
            return Apresentacao.objects.filter(id=self.kwargs['id'])
        else:
            return Apresentacao.objects.none()


class ApresentacaoList(generics.ListAPIView):
    queryset = Apresentacao.objects.all()
    serializer_class = ApresentacaoListSerializer
    pagination_class = SmallResultsSetPagination


