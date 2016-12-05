from rest_framework import serializers

from api.models.principio_ativo import PrincipioAtivo


class PrincipioAtivoSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = PrincipioAtivo
        fields = '__all__'
