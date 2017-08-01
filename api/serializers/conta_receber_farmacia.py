from rest_framework import serializers

from api.models.conta_receber_farmacia import ContaReceberFarmacia


class ContaReceberFarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaReceberFarmacia
        fields = ('id', 'data_credito', 'data_vencimento', 'valor_bruto', 'valor_liquido', 'status')

