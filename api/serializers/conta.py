import locale

from rest_framework import serializers

from api.models.boleto import Boleto
from api.models.conta import Conta
from api.models.conta_pagar import ContaPagar


class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = ('pdf', 'codigo_de_barras')

    def get_pdf(self, obj):
        request = self.context.get('request')
        photo_url = obj.pdf.url
        return request.build_absolute_uri(photo_url)


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
            'boleto', 'data_vencimento', 'valor_total', 'status', 'tipo', 'id'
        )
