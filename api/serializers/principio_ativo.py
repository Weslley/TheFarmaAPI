from rest_framework import serializers

from api.models.principio_ativo import PrincipioAtivo


class PrincipioAtivoSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = PrincipioAtivo
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class PrincipioAtivoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrincipioAtivo
        fields = ('id', 'nome')
