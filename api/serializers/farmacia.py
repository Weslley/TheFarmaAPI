from rest_framework import serializers

from api.models.farmacia import Farmacia


class FarmaciaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = ('cnpj', 'nome_fantasia', 'razao_social')


class FarmaciaSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Farmacia
        fields = '__all__'
