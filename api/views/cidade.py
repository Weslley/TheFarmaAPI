# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.cidade import Cidade
from api.pagination import SmallResultsSetPagination
from api.serializers.cidade import CidadeSerializer


class CidadeList(generics.ListAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    pagination_class = SmallResultsSetPagination

