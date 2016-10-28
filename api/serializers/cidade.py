from rest_framework import serializers

from api.models.cidade import Cidade
from api.serializers.uf import UfSerializer


class CidadeSerializer(serializers.ModelSerializer):
    uf = UfSerializer()

    class Meta:
        model = Cidade
        fields = '__all__'


class CidadeBasicSerializer(serializers.ModelSerializer):
    uf = serializers.CharField(source='uf.sigla')

    class Meta:
        model = Cidade
        fields = ('ibge', 'nome', 'uf')
