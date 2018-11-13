from rest_framework import generics

from api.mixins.base import IsAuthenticatedRepresentanteMixin
from api.models.conta import Conta
from api.serializers.conta import ContaSerializer
from api.pagination import SmallResultsSetPagination


class ContaList(generics.ListAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Lista as contas de faturamento relacionadas ao 
    representante que fez a requisicao
    """
    serializer_class = ContaSerializer
    pagination_class = SmallResultsSetPagination

    def get_representante(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia

    def get_queryset(self):
        representante = self.get_representante()
        return Conta.objects.filter(
            farmacia__representantes=representante
        ).order_by('-data_vencimento')


class ContaRetrieve(generics.RetrieveAPIView, IsAuthenticatedRepresentanteMixin):
    """
    Detalhe das conta de faturamento
    """
    serializer_class = ContaSerializer
    queryset = Conta.objects.all()