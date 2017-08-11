from rest_framework import generics

from api.pagination import SmallResultsSetPagination
from api.models.secao import Secao
from api.serializers.secao import SecaoListSerializer, SecaoDetailSerializer


class SecaoList(generics.ListAPIView):
    queryset = Secao.objects.all()
    serializer_class = SecaoListSerializer
    pagination_class = SmallResultsSetPagination


class SecaoDetail(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    queryset = Secao.objects.all()
    serializer_class = SecaoDetailSerializer
