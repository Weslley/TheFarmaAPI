# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models import Cidade
from api.pagination import SmallResultsSetPagination
from api.serializers import CidadeSerializer


class CidadeList(generics.ListAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    pagination_class = SmallResultsSetPagination
