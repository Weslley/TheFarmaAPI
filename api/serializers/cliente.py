from rest_framework import serializers
from api.models.cliente import Cliente


class ClienteCreateSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(max_length=30)
    sobrenome = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField(required=True)
    senha = serializers.CharField(max_length=30, style={'input_type': 'password'})
    confirmacao_senha = serializers.CharField(max_length=30, style={'input_type': 'password'})

    class Meta:
        model = Cliente
        fields = (
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
