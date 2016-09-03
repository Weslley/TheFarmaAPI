# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models import Farmacia
from api.pagination import SmallResultsSetPagination
from api.serializers import FarmaciaSerializer, FarmaciaListSerializer


class FarmaciaList(generics.ListAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination


class FarmaciaDetail(generics.RetrieveAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer
