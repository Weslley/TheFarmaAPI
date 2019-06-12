# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from api.mixins.base import (IsAuthenticatedMixin,
                             IsAuthenticatedRepresentanteMixin)
from api.models.representante_legal import RepresentanteLegal
from api.models.farmacia import Farmacia
from api.serializers.representante_legal import RepresentanteSerializer, RepresentanteFarmaciaSerializer

class RepresentanteRetrieve(generics.RetrieveUpdateAPIView, IsAuthenticatedRepresentanteMixin):
    queryset = RepresentanteLegal.objects.all()
    serializer_class = RepresentanteSerializer

    def get_object(self):
    	self.check_object_permissions(self.request, self.request.user.representante_farmacia)
    	print(self.request.user.representante_farmacia)
    	return self.request.user.representante_farmacia


class RepresentanteFarmaciaView(generics.RetrieveUpdateAPIView):
    queryset = RepresentanteLegal.objects.all()
    serializer_class = RepresentanteFarmaciaSerializer
    """
    Retorna os representantes com base no ID
    """
