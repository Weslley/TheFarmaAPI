from rest_framework import serializers
from api.models.medicamento import Medicamento
from api.serializers.apresentacao import ApresentacaoListSerializer


class MedicamentoSerializer(serializers.ModelSerializer):
    apresentacoes = ApresentacaoListSerializer(many=True)

    class Meta:
        model = Medicamento
        fields = '__all__'


class MedicamentoListSerializer(serializers.HyperlinkedModelSerializer):
    nome = serializers.ReadOnlyField()
    medicamento = serializers.HyperlinkedIdentityField(view_name='medicamento-view', lookup_field='id', format='html')

    class Meta:
        model = Medicamento
        fields = ('nome', 'medicamento')
