# -*- coding: utf-8 -*-

from rest_framework import generics
from api.models import Laboratorio
from api.serializers import LaboratorioSerializer


class LaboratorioList(generics.ListAPIView):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
