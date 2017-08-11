from rest_framework import generics

from api.pagination import SmallResultsSetPagination
from api.models.bairro import Bairro
from api.serializers.bairro import BairroListSerializer


class BairroList(generics.ListAPIView):
    serializer_class = BairroListSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        return Bairro.objects.filter(cidade__ibge=self.kwargs['ibge'])
