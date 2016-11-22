# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.laboratorio import Laboratorio
from api.pagination import SmallResultsSetPagination
from api.serializers.laboratorio import LaboratorioSerializer


class LaboratorioList(generics.ListAPIView):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    pagination_class = SmallResultsSetPagination


class LaboratorioExport(APIView):
    def get(self, request, format=None):
        try:
            firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
            auth = firebase.auth()
            user = auth.current_user
            db = firebase.database()
            data = db.child('laboratorios').get()
            resultado = [pyre for pyre in data.pyres if pyre]
            return Response(resultado)
        except Exception as err:
            return Response({'detail': 'Erro ao carregar os dados - {}'.format(str(err))})