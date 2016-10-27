# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.farmacia import Farmacia
from api.mixins.base import IsAuthenticatedMixin
from api.pagination import SmallResultsSetPagination
from api.serializers.farmacia import FarmaciaSerializer, FarmaciaListSerializer


class FarmaciaList(generics.ListAPIView, IsAuthenticatedMixin):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination


class FarmaciaDetail(generics.RetrieveAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer
