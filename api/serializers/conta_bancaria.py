from rest_framework import serializers

from api.models.conta_bancaria import ContaBancaria


class ContaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaBancaria
        fields = ('banco', 'numero_agencia', 'digito_agencia', 'numero_conta', 'digito_conta')

