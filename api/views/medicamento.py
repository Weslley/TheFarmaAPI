# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.medicamento import Medicamento
from api.pagination import SmallResultsSetPagination, StandardResultsSetPagination
from api.serializers.medicamento import *


class MedicamentoList(generics.ListAPIView):
    """
    Listagem dos medicamentos cadastrados
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoListSerializer
    pagination_class = StandardResultsSetPagination




class MedicamentoRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        if 'id' in self.kwargs and self.kwargs['id']:
            return Medicamento.objects.filter(id=self.kwargs['id'])
        else:
            return Medicamento.objects.none()
