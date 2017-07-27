from rest_framework import generics
from rest_framework.response import Response

from api.models.atualizacao import Atualizacao
from api.serializers.atualizacao import AtualizacaoSerializer


class UltimaAtualizacao(generics.GenericAPIView):
    serializer_class = AtualizacaoSerializer

    def get(self, request, format=None):
        instance = Atualizacao.objects.order_by('id').last()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
