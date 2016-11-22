from django.conf import settings
from pyrebase import pyrebase
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.tabela_preco import TabelaPreco
from api.pagination import SmallResultsSetPagination
from api.serializers.tabela_preco import TabelaPrecoSerializer


class TabelaPrecoList(generics.ListAPIView):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer
    pagination_class = SmallResultsSetPagination


class TabelaPrecoExport(APIView):
    def get(self, request, format=None):
        try:
            firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
            auth = firebase.auth()
            user = auth.current_user
            db = firebase.database()
            data = db.child('tabelas_preco').get()
            resultado = [pyre.item[1] for pyre in data.pyres if pyre]
            return Response(resultado)
        except Exception as err:
            print(err)
            return Response({'detail': 'Erro ao carregar os dados'})

