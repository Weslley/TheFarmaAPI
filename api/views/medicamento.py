# -*- coding: utf-8 -*-

from rest_framework import generics

from api.filters import MedicamentoFilter, OrderingFilter
from api.models.medicamento import Medicamento
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import SmallResultsSetPagination, StandardResultsSetPagination
from api.serializers.medicamento import *


class MedicamentoList(generics.ListAPIView):
    """
    Listagem dos medicamentos cadastrados
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = MedicamentoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)


class MedicamentoRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        if 'id' in self.kwargs and self.kwargs['id']:
            return Medicamento.objects.filter(id=self.kwargs['id'])
        else:
            return Medicamento.objects.none()

