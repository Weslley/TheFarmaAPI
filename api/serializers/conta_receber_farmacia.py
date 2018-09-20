import locale

from rest_framework import serializers

from api.models.conta_pagar import ContaPagar


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')



class AnnotationContaReceberSerializer(serializers.Serializer):
    data_vencimento = serializers.DateTimeField()
    valor_liquido = serializers.CharField()