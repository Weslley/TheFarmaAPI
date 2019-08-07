# -*- coding: utf-8 -*-

from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin, IsClienteAuthenticatedMixin
from api.models.farmacia import Farmacia
from api.pagination import SmallResultsSetPagination
from api.serializers.farmacia import FarmaciaListSerializer, FarmaciaUpdateSerializer, FarmaciaSerializer


class FarmaciaList(generics.ListAPIView, IsAuthenticatedMixin):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination

class FarmaciaDetail(generics.RetrieveAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer

class FarmaciaRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmaciaUpdateSerializer
    queryset = Farmacia.objects.all()
    
class FarmaciaRetrieve(generics.RetrieveAPIView, IsClienteAuthenticatedMixin):
    lookup_url_kwarg = 'id'
    serializer_class = FarmaciaListSerializer
    queryset = Farmacia.objects.all()