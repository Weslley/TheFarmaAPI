from rest_framework import generics

from api.mixins.base import SyncApiMixin
from api.models.uf import Uf
from api.pagination import LargeResultsSetPagination
from api.serializers.uf import UfReduzidoSerializer, UfSerializer


class UfList(generics.ListAPIView):
    queryset = Uf.objects.all()
    serializer_class = UfReduzidoSerializer
    pagination_class = LargeResultsSetPagination


class UfSync(generics.ListAPIView, SyncApiMixin):
    queryset = Uf.objects.all()
    serializer_class = UfReduzidoSerializer
    pagination_class = LargeResultsSetPagination


class UfExport(generics.ListAPIView):
    queryset = Uf.objects.all()
    serializer_class = UfReduzidoSerializer
    pagination_class = LargeResultsSetPagination
