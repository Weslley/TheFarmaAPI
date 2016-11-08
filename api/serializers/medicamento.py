from rest_framework import serializers
from api.models.medicamento import Medicamento
from api.serializers.apresentacao import ApresentacaoListSerializer


class MedicamentoSerializer(serializers.ModelSerializer):
    apresentacoes = ApresentacaoListSerializer(many=True)

    class Meta:
        model = Medicamento
        fields = '__all__'


class MedicamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ('nome', 'id')


class MedicamentoExportSerializer(serializers.ModelSerializer):
    apresentacoes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')

    class Meta:
        model = Medicamento
        fields = '__all__'
