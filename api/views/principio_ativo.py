# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models import PrincipioAtivo
from api.pagination import SmallResultsSetPagination
from api.serializers import PrincipioAtivoSerializer


class PrincipioAtivoList(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = SmallResultsSetPagination
