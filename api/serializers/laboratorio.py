from rest_framework import serializers

from api.models.laboratorio import Laboratorio


class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = '__all__'
