# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.laboratorio import Laboratorio
from api.pagination import SmallResultsSetPagination, LargeResultsSetPagination
from api.serializers.laboratorio import LaboratorioSerializer


class LaboratorioList(generics.ListAPIView):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = SmallResultsSetPagination


class LaboratorioSync(generics.ListAPIView, SyncApiMixin):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = LargeResultsSetPagination


class LaboratorioExport(generics.ListAPIView):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
