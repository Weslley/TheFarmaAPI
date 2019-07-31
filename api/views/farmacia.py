# -*- coding: utf-8 -*-

from rest_framework import generics

from api.mixins.base import IsAuthenticatedMixin
from api.models.farmacia import Farmacia
from api.pagination import SmallResultsSetPagination
from api.serializers.farmacia import FarmaciaListSerializer, FarmaciaUpdateSerializer, FarmaciaSerializer


class FarmaciaList(generics.ListAPIView, IsAuthenticatedMixin):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination

class FarmaciaDetail(generics.RetrieveAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer

class FarmaciaRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmaciaUpdateSerializer
    queryset = Farmacia.objects.all()
    
    '''
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        #verifica se tem veiculo associado
        if hasattr(self.get_object(),'veiculo'):
            raise serializers.ValidationError({'confirmacao':'Esse modulo contem um veiculo associado, exige uma confirmacao para deletar'})
        else:
            #cria o log
            criar_log({
                'acao':LogSistemaText.DELETE,
                'entidade':'modulo',
                'entidade_id':obj.id,
                'usuario':self.request.user
            })
            return super().delete(request,*args, **kwargs)
    '''