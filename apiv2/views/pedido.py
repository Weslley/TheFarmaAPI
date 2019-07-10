from rest_framework import generics, response
from apiv2.serializers.pedido import PedidoCreateSerializer
from rest_framework import permissions
from api.models.pedido import Pedido
from api.consumers.farmacia import FarmaciaConsumer, PropostaSerializer

class PedidoCreateListView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    #permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PedidoCreateSerializer
        else:
            return PedidoCreateSerializer
    
    def get(self,request,*args,**kwargs):
        p = Pedido.objects.last()
        ps = PropostaSerializer(p)
        FarmaciaConsumer.send(ps.data,id=8)
        return response.Response()