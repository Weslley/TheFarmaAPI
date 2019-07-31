from rest_framework import serializers

from api.models.uf import Uf


class UfSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Uf
        fields = '__all__'


class UfReduzidoSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Uf
        fields = ('sigla', 'icms', 'data_atualizacao')

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)
