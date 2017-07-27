from rest_framework import serializers
from api.models.representante_legal import RepresentanteLegal
from api.serializers.endereco import EnderecoSerializer
from api.serializers.farmacia import FarmaciaListSerializer


class RepresentanteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    farmacia = FarmaciaListSerializer()

    class Meta:
        model = RepresentanteLegal
        exclude = ('id',)
