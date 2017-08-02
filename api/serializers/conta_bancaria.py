from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import empty

from api.models.banco import Banco
from api.models.conta_bancaria import ContaBancaria


class ContaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaBancaria
        fields = ('banco', 'numero_agencia', 'digito_agencia', 'numero_conta', 'digito_conta')

    def run_validation(self, data=empty):
        if isinstance(data, OrderedDict):
            return data

        value = super(ContaBancariaSerializer, self).run_validation(data)
        return value
