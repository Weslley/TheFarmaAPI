from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.banco import Banco
from api.pagination import SmallResultsSetPagination
from api.serializers.banco import BancoSerializer


class BancoList(generics.ListAPIView, IsAuthenticatedMixin):
    serializer_class = BancoSerializer
    pagination_class = SmallResultsSetPagination
    queryset = Banco.objects.all()
