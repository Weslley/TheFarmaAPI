from rest_framework import serializers
from api.models.cliente import Cliente
from api.serializers.user import DetailUserSerializer, DetailUserNoTokenSerializer


class ClienteSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField(required=False, allow_null=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    nome = serializers.CharField(max_length=60, source='usuario.get_full_name')
    email = serializers.EmailField(source='usuario.email')
    token = serializers.CharField(read_only=True, source='usuario.auth_token.key')

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
            'nome',
            'email',
            'token'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'facebook_id': {'read_only': True},
        }

    def get_nome(self, obj):
        return obj.usuario.get_full_name()


class ClienteNoTokenSerializer(serializers.ModelSerializer):
    usuario = DetailUserNoTokenSerializer()
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
            'facebook_id': {'read_only': True},
        }
