from rest_framework import generics

from api.models.secao import Secao
from api.pagination import SmallResultsSetPagination
from api.serializers.secao import SecaoListSerializer


class SecaoList(generics.ListAPIView):
    queryset = Secao.objects.all()
    serializer_class = SecaoListSerializer
    pagination_class = SmallResultsSetPagination
