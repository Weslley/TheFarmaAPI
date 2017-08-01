from rest_framework import serializers

from api.models.banco import Banco
from api.models.conta_bancaria import ContaBancaria


class ContaBancariaSerializer(serializers.ModelSerializer):
    banco = serializers.PrimaryKeyRelatedField(queryset=Banco.objects.all())

    class Meta:
        model = ContaBancaria
        fields = ('banco', 'numero_agencia', 'digito_agencia', 'numero_conta', 'digito_conta')
