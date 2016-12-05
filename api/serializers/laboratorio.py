from rest_framework import serializers

from api.models.laboratorio import Laboratorio


class LaboratorioSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Laboratorio
        fields = '__all__'
