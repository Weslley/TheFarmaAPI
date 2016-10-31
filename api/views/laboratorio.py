# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.laboratorio import Laboratorio
from api.pagination import SmallResultsSetPagination
from api.serializers.laboratorio import LaboratorioSerializer


class LaboratorioList(generics.ListAPIView):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = SmallResultsSetPagination
