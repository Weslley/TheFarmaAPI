from rest_framework import serializers

from api.models.farmacia import Farmacia


class FarmaciaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = ('cnpj', 'nome_fantasia')


class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'