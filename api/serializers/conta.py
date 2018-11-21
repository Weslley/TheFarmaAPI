import locale

from rest_framework import serializers

from api.models.boleto import Boleto
from api.models.conta import Conta
from api.models.conta_pagar import ContaPagar


class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = ('pdf', 'codigo_de_barras')


class ContaMinimalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data_vencimento = serializers.DateTimeField()
    valor_total = serializers.CharField()
    status = serializers.IntegerField()
    tipo = serializers.IntegerField()


class ContaSerializer(serializers.ModelSerializer):
    boleto = BoletoSerializer()
    class Meta:
        model = Conta
        fields = (
            'boleto', 'data_emissao', 'data_vencimento',
            'valor_total', 'status', 'tipo', 'id'
        )
