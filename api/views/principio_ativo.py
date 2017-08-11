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


class PrincipioAtivoList(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = SmallResultsSetPagination


class PrincipioAtivoSync(generics.ListAPIView, SyncApiMixin):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = LargeResultsSetPagination


class PrincipioAtivoExport(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = LargeResultsSetPagination
