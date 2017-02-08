from api.models.estoque import Estoque
from api.serializers.estoque import *
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from misc.pusher_message import Message
from django.db import transaction


class EstoqueCreateUpdate(CreateAPIView):
    """
    Cria ou atualiza o estoque de uma apresentação
    """
    queryset = Estoque.objects.all()
    serializer_class = EstoqueCreateUpdateSerializer
    objects = None
    estoque = None

    def update(self, request, *args, **kwargs):

        for key in self.objects.keys():
            setattr(self.estoque, key, self.objects[key])

        self.estoque.save()
        pusher_conn = Message('default')
        pusher_conn.send(event='reload_estoque', data={'mensagem': None})
        return Response(request.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            if self.exist_estoque(request):
                return self.update(request, *args, **kwargs)
            else:
                return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.estoque = Estoque.objects.create(**self.objects)
        pusher_conn = Message('default')
        pusher_conn.send(event='reload_estoque', data={'mensagem': None})
        return Response(request.data, status=status.HTTP_201_CREATED)

    def exist_estoque(self, request):
        """
        Verifica se existe ou não estoque da apresentação de acordo com a farmacia
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.objects = {
            'apresentacao': serializer.validated_data.get('codigo_barras'),
            'farmacia': request.user.representante_farmacia.farmacia
        }
        exist = False
        try:
            self.estoque = Estoque.objects.get(**self.objects)
            exist = True
        except Estoque.DoesNotExist:
            pass

        self.objects['quantidade'] = serializer.validated_data.get('quantidade')
        self.objects['valor'] = serializer.validated_data.get('valor')

        return exist
