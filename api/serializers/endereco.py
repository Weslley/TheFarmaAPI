from rest_framework import serializers

from api.models.endereco import Endereco
from api.serializers.bairro import BairroSerializer
from api.serializers.cidade import CidadeBasicSerializer


class EnderecoSerializer(serializers.ModelSerializer):
    cidade = CidadeBasicSerializer()
    bairro = BairroSerializer()

    class Meta:
        model = Endereco
        fields = '__all__'


