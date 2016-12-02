from rest_framework import serializers
from api.models.atualizacao import Atualizacao


class AtualizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atualizacao
        fields = ('data', )
