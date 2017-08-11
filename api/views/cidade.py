# -*- coding: utf-8 -*-

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from api.filters import CidadeFilter, OrderingFilter
from api.models.cidade import Cidade
from api.pagination import SmallResultsSetPagination
from api.serializers.cidade import CidadeSerializer, CoberturaCidadeSerializer


class CidadeList(generics.ListAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CidadeFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)

    def get_serializer_class(self):
        consulta = self.request.GET.get('q')

        if consulta and consulta == 'r':
            return CoberturaCidadeSerializer
        else:
            return CidadeSerializer


class CidadeDetail(generics.RetrieveAPIView):
    lookup_url_kwarg = 'ibge'
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
