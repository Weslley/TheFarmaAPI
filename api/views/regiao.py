from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import SyncApiMixin
from api.models.regiao import Regiao
from api.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from api.serializers.regiao import RegiaoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import OrderingFilter, RegiaoFilter


class RegiaoList(generics.ListAPIView):
    queryset = Regiao.objects.all()
    serializer_class = RegiaoSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = RegiaoFilter
    ordering_fields = ('nome', '-nome')
    ordering = ('nome',)


class RegiaoRetrieve(generics.RetrieveAPIView):
    queryset = Regiao.objects.all()
    serializer_class = RegiaoSerializer
