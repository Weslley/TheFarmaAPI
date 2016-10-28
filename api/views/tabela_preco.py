from rest_framework import generics

from api.models.tabela_preco import TabelaPreco
from api.pagination import SmallResultsSetPagination
from api.serializers.tabela_preco import TabelaPrecoSerializer


class TabelaPrecoList(generics.ListAPIView):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer
    pagination_class = SmallResultsSetPagination