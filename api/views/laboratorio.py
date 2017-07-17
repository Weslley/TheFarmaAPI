# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.fabricante import Fabricante
from api.pagination import SmallResultsSetPagination, LargeResultsSetPagination
from api.serializers.laboratorio import LaboratorioSerializer


class LaboratorioList(generics.ListAPIView):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = SmallResultsSetPagination


class LaboratorioSync(generics.ListAPIView, SyncApiMixin):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = LargeResultsSetPagination


class LaboratorioExport(generics.ListAPIView):
    queryset = Fabricante.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = LargeResultsSetPagination
