from rest_framework import serializers
from api.models.atualizacao import Atualizacao


class AtualizacaoSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Atualizacao
        fields = ('data', )

    def get_data(self, obj):
        return int(obj.data.timestamp() * 1000)
