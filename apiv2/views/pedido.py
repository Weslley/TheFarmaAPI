from rest_framework import generics
from apiv2.serializers.pedido import PedidoCreateSerializer
from rest_framework import permissions
from api.models.pedido import Pedido

class PedidoCreateListView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    #permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            raise NotImplementedError()
        else:
            return PedidoCreateSerializer