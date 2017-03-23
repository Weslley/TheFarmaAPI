from rest_framework import serializers

from api.models.secao import Secao
from api.serializers.subsecao import SubsecaoListSerializer


class SecaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secao
        fields = ('id', 'nome', 'imagem')


class SecaoDetailSerializer(serializers.ModelSerializer):
    subsecoes = SubsecaoListSerializer(many=True)

    class Meta:
        model = Secao
        fields = ('id', 'nome', 'imagem', 'subsecoes')
