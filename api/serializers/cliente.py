from rest_framework import serializers
from api.models.cliente import Cliente


class ClienteCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(source='usuario.first_name', max_length=30, read_only=True)
    sobrenome = serializers.CharField(source='usuario.last_name', max_length=30, read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
    senha = serializers.CharField(max_length=30, style={'input_type': 'password'}, read_only=True)
    confirmacao_senha = serializers.CharField(max_length=30, style={'input_type': 'password'}, read_only=True)

    class Meta:
        model = Cliente
        fields = (
            'id',
            'nome',
            'sobrenome',
            'email',
            'data_nascimento',
            'sexo',
            'foto',
            'cpf',
            'telefone',
            'senha',
            'confirmacao_senha'
        )

    def create(self, validated_data):
        validated_data['usuario'] = self.context['view'].usuario
        instance = super(ClienteCreateSerializer, self).create(validated_data)
        return instance
