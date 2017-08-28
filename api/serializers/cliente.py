from rest_framework import serializers
from api.models.cliente import Cliente
from api.serializers.user import DetailUserSerializer


class ClienteSerializer(serializers.ModelSerializer):
    usuario = DetailUserSerializer()
    data_nascimento = serializers.DateField(required=False, allow_null=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y'])

    class Meta:
        model = Cliente
        fields = (
            'id',
            'data_nascimento',
            'sexo',
            'foto',
            'cpf',
            'celular',
            'facebook_id',
            'usuario'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
