# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models.representante_legal import RepresentanteLegal
from api.mixins.base import IsAuthenticatedMixin
from api.serializers.representante_legal import RepresentanteSerializer


class RepresentanteRetrieve(generics.RetrieveUpdateAPIView, IsAuthenticatedMixin):
    queryset = RepresentanteLegal.objects.all()
    serializer_class = RepresentanteSerializer

    def get_object(self):
        user = self.request.user

        if hasattr(user, 'representante_farmacia') and user.representante_farmacia:
            obj = user.representante_farmacia
        else:
            raise Exception('Usuário não é representante de farmácia.')

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
