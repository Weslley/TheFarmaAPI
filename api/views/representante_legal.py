# -*- coding: utf-8 -*-

from rest_framework import generics

from api.mixins.base import (IsAuthenticatedMixin,
                             IsAuthenticatedRepresentanteMixin)
from api.models.representante_legal import RepresentanteLegal
from api.serializers.representante_legal import RepresentanteSerializer


class RepresentanteRetrieve(generics.RetrieveUpdateAPIView, IsAuthenticatedRepresentanteMixin):
    queryset = RepresentanteLegal.objects.all()
    serializer_class = RepresentanteSerializer

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user.representante_farmacia)
        return self.request.user.representante_farmacia
