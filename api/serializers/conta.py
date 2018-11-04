import locale

from rest_framework import serializers

from api.models.conta_pagar import ContaPagar


class ContaSerializer(serializers.Serializer):
    data_vencimento = serializers.DateTimeField()
    valor_total = serializers.CharField()
    status = serializers.IntegerField()
    tipo = serializers.IntegerField()