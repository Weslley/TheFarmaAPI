from rest_framework import serializers

from api.models.uf import Uf


class UfSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Uf
        fields = '__all__'


class UfReduzidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf
        fields = ('sigla', )