from rest_framework import generics
from api.models.representante_legal import RepresentanteLegal
from api.mixins.base import IsAuthenticatedMixin, IsAuthenticatedRepresentanteMixin
from api.serializers.representante_legal import RepresentanteSerializer


class ResumoFinanceiro(generics.GenericAPIView, IsAuthenticatedRepresentanteMixin):
    queryset = RepresentanteLegal.objects.all()
    serializer_class = RepresentanteSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia
