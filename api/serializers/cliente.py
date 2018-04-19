from rest_framework import serializers
from rest_framework.compat import set_many
from rest_framework.utils import model_meta
from api.models.cliente import Cliente
from api.serializers.user import DetailUserSerializer, DetailUserNoTokenSerializer
from django.contrib.auth.models import User


def split_name(palavra, tamanho=30, quantidade=2):
    lista_nome = ['' for n in range(quantidade)]
    index = 0
    split_nome = palavra.split()
    for palavra in split_nome:
        if index == quantidade:
            break
        if len(lista_nome[index]) + 1 + len(palavra) <= tamanho:
            lista_nome[index] += ' {}'.format(palavra)
            lista_nome[index] = (lista_nome[index]).strip()
        else:
            index += 1
            if len(lista_nome[index]) + 1 + len(palavra) <= tamanho:
                lista_nome[index] += ' {}'.format(palavra)
                lista_nome[index] = (lista_nome[index]).strip()
            else:
                break

    return lista_nome


class ClienteSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField(required=False, allow_null=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    nome = serializers.CharField(max_length=60, source='usuario.get_full_name', required=False)
    email = serializers.EmailField(source='usuario.email', required=False)
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
        }

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        usuario = validated_data.pop('usuario', None)
        if usuario:
            nome = usuario.pop('get_full_name', None)
            if nome:
                first_name = split_name(nome)[0]
                last_name = split_name(nome)[1]
                instance.usuario.first_name = first_name
                instance.usuario.last_name = last_name
                instance.usuario.save()

            email = usuario.pop('email', None)
            if email:
                instance.usuario.email = email
                instance.usuario.save()

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


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
