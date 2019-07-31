# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.principio_ativo import PrincipioAtivo
from api.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from api.serializers.principio_ativo import PrincipioAtivoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import OrderingFilter, PrincipioAtivoFilter


class PrincipioAtivoList(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PrincipioAtivoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)


class PrincipioAtivoRetrieve(generics.RetrieveAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    

class PrincipioAtivoSync(generics.ListAPIView, SyncApiMixin):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = LargeResultsSetPagination


class PrincipioAtivoExport(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = LargeResultsSetPagination
