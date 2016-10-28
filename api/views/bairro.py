from rest_framework import generics

from api.models.bairro import Bairro
from api.pagination import SmallResultsSetPagination
from api.serializers.bairro import BairroListSerializer


class BairroList(generics.ListAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroListSerializer
    pagination_class = SmallResultsSetPagination