from rest_framework import serializers
from api.models.bairro import Bairro
from api.serializers.cidade import CidadeBasicSerializer


class BairroListSerializer(serializers.ModelSerializer):
    cidade = CidadeBasicSerializer()

    class Meta:
        model = Bairro
        fields = '__all__'