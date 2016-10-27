# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.medicamento import Medicamento
from api.pagination import SmallResultsSetPagination
from api.serializers.medicamento import MedicamentoSerializer


class MedicamentoList(generics.ListAPIView):
    """
    Listagem dos medicamentos cadastrados
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    pagination_class = SmallResultsSetPagination
