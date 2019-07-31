from rest_framework import serializers

from api.models.regiao import Regiao


class RegiaoSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Regiao
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class RegiaoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiao
        fields = ('id', 'nome')
