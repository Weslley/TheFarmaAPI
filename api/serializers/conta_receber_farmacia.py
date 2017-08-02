import locale
from rest_framework import serializers

from api.models.conta_receber_farmacia import ContaReceberFarmacia

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ContaReceberFarmaciaSerializer(serializers.ModelSerializer):
    valor_bruto = serializers.SerializerMethodField()
    valor_liquido = serializers.SerializerMethodField()

    class Meta:
        model = ContaReceberFarmacia
        fields = ('id', 'data_credito', 'data_vencimento', 'valor_bruto', 'valor_liquido', 'status')

    def get_valor_bruto(self, obj):
        return locale.currency(obj.valor_bruto, grouping=True, symbol=None)

    def get_valor_liquido(self, obj):
        return locale.currency(obj.valor_liquido, grouping=True, symbol=None)