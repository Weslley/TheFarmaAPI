# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.fabricante import Fabricante
from api.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from api.serializers.laboratorio import LaboratorioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import OrderingFilter, LaboratorioFilter


class LaboratorioList(generics.ListAPIView):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = LaboratorioFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)


class LaboratorioSync(generics.ListAPIView, SyncApiMixin):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = LargeResultsSetPagination


class LaboratorioExport(generics.ListAPIView):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = LargeResultsSetPagination



class LaboratorioRetrieve(generics.RetrieveAPIView):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer