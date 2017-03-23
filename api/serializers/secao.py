from rest_framework import serializers

from api.models.secao import Secao


class SecaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secao
        fields = ('id', 'nome', 'imagem')
