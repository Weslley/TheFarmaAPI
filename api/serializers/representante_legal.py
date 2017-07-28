from rest_framework import serializers
from api.models.representante_legal import RepresentanteLegal
from api.serializers.endereco import EnderecoSerializer
from api.serializers.farmacia import FarmaciaListSerializer
from api.serializers.user import RepresentanteUserSerializer


class RepresentanteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    farmacia = FarmaciaListSerializer()
    usuario = RepresentanteUserSerializer()

    class Meta:
        model = RepresentanteLegal
        exclude = ('id',)
