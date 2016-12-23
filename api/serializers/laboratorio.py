from rest_framework import serializers

from api.models.laboratorio import Laboratorio


class LaboratorioSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Laboratorio
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)
