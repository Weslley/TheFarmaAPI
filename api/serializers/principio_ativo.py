from rest_framework import serializers

from api.models.principio_ativo import PrincipioAtivo


class PrincipioAtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrincipioAtivo
        fields = '__all__'
