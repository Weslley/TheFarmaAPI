from rest_framework import serializers
from api.models.endereco import Endereco

class EnderecoFarmaciaSerializer(serializers.ModelSerializer):
    cidade = serializers.SerializerMethodField()

    class Meta:
        model = Endereco
        fields = (
            'cep',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
        )
    
    def get_cidade(self, obj):
        if obj.cidade:
            return str(obj.cidade)
        return None
    