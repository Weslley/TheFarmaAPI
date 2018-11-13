import locale

from rest_framework import serializers

from api.models.conta import Conta
from api.models.conta_pagar import ContaPagar


class ContaMinimalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data_vencimento = serializers.DateTimeField()
    valor_total = serializers.CharField()
    status = serializers.IntegerField()
    tipo = serializers.IntegerField()


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = (
            'data_vencimento', 'valor_total', 'status', 'tipo', 'id'
        )
