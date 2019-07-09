from rest_framework import generics
from apiv2.serializer.pedido import PedidoCreateSerializer
from api.models.pedido import Pedido

class PedidoCreateListView(generics.ListCreateAPIView):
    serializer_class = PedidoCreateSerializer
    queryset = Pedido.objects.all()