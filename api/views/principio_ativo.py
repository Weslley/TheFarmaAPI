# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.principio_ativo import PrincipioAtivo
from api.pagination import SmallResultsSetPagination
from api.serializers.principio_ativo import PrincipioAtivoSerializer


class PrincipioAtivoList(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = SmallResultsSetPagination
