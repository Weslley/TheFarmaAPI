# -*- coding: utf-8 -*-

from rest_framework import generics

from api.consumers.farmacia import FarmaciaConsumer
from api.mixins.base import IsAuthenticatedMixin
from api.models.farmacia import Farmacia
from api.pagination import SmallResultsSetPagination
from api.serializers.farmacia import FarmaciaListSerializer, FarmaciaSerializer


class FarmaciaList(generics.ListAPIView, IsAuthenticatedMixin):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination


class FarmaciaDetail(generics.RetrieveAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer


class FarmaciaPedidos(generics.ListAPIView):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaListSerializer
    pagination_class = SmallResultsSetPagination

    def get(self, request, *args, **kwargs):
        farmacias = [f.id for f in Farmacia.objects.all()]
        # consumer = FarmaciaConsumer()
        # consumer.send({
        #     "farmacias": farmacias,
        #     "content": {
        #         "id": "123",
        #         "tempo": 180,
        #         "delivery": True,
        #         "status": 0,
        #         "troco": 40,
        #         "forma_pagamento": 0,
        #         "cliente": "Philippe Valfok",
        #         "endereco": {
        #             "logradouro": "Rua selecionada da entrega",
        #             "cep": "64222555",
        #             "cidade": "Cidade",
        #             "uf": "Piauí",
        #             "numero": 123,
        #             "complemento": "",
        #         },
        #         "itens": [
        #             {
        #                 "id": 12,
        #                 "apresentacao": {
        #                     "id": 2,
        #                     "nome": "Sinvastativa",
        #                     "fabricante": "Bayer"
        #                 },
        #                 "quantidade": 4,
        #                 "PMC": 33.50,
        #                 "imagem": "http://www.farmaecia.com.br/img/gen/embalagem-medicamento-generico.gif"
        #             },
        #             {
        #                 "id": 13,
        #                 "apresentacao": {
        #                     "id": 4,
        #                     "nome": "Puran T4",
        #                     "fabricante": "Bayer"
        #                 },
        #                 "quantidade": 2,
        #                 "PMC": 18.70,
        #                 "imagem": "http://www.farmaecia.com.br/img/gen/embalagem-medicamento-generico.gif"
        #             },
        #             {
        #                 "id": 14,
        #                 "apresentacao": {
        #                     "id": 2,
        #                     "nome": "Neosaldina",
        #                     "fabricante": "Bayer"
        #                 },
        #                 "quantidade": 1,
        #                 "PMC": 4.0,
        #                 "imagem": "http://www.farmaecia.com.br/img/gen/embalagem-medicamento-generico.gif"
        #             },
        #         ]
        #     }
        # })
        return super(FarmaciaPedidos, self).get(request, *args, **kwargs)
