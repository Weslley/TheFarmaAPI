# -*- coding: utf-8 -*-
from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.principio_ativo import PrincipioAtivo
from api.pagination import SmallResultsSetPagination
from api.serializers.principio_ativo import PrincipioAtivoSerializer


class PrincipioAtivoList(generics.ListAPIView):
    queryset = PrincipioAtivo.objects.all()
    serializer_class = PrincipioAtivoSerializer
    pagination_class = SmallResultsSetPagination


class PrincipioAtivoExport(APIView):
    def get(self, request, format=None):
        try:
            firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
            auth = firebase.auth()
            user = auth.current_user
            db = firebase.database()
            data = db.child('principios_ativos').get()
            resultado = [pyre.item[1] for pyre in data.pyres if pyre]
            return Response(resultado)
        except Exception as err:
            print(err)
            return Response({'detail': 'Erro ao carregar os dados'})