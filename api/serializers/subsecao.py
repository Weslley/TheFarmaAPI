from rest_framework import serializers

from api.models.subsecao import Subsecao


class SubsecaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsecao
        fields = ('id', 'nome')
