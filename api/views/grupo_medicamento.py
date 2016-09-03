# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models import GrupoMedicamento
from api.pagination import SmallResultsSetPagination
from api.serializers import GrupoMedicamentoSerializer


class GrupoMedicamentoList(generics.ListAPIView):
    queryset = GrupoMedicamento.objects.all()
    serializer_class = GrupoMedicamentoSerializer
    pagination_class = SmallResultsSetPagination
