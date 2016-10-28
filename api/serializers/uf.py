from rest_framework import serializers

from api.models.uf import Uf


class UfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf
        fields = '__all__'
