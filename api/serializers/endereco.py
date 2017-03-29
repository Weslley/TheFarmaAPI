from rest_framework import serializers

from api.models.endereco import Endereco


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


