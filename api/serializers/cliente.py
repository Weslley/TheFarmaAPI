from rest_framework import serializers
from rest_framework.compat import set_many
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from api.models.cliente import Cliente
from api.serializers.user import DetailUserSerializer


class ClienteSerializer(serializers.ModelSerializer):
    usuario = DetailUserSerializer()

    class Meta:
        model = Cliente
        fields = (
            'id',
            'data_nascimento',
            'sexo',
            'foto',
            'cpf',
            'telefone',
            'facebook_id',
            'usuario'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # Salvando o usuario
        if 'usuario' in validated_data:
            usuario = instance.usuario
            user_info = model_meta.get_field_info(usuario)
            user_validated_data = dict(validated_data['usuario'])

            for attr, value in user_validated_data.items():
                if attr in user_info.relations and user_info.relations[attr].to_many:
                    set_many(usuario, attr, value)
                else:
                    setattr(usuario, attr, value)
            usuario.save()

        # Salvando o cliente
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr != 'usuario':
                if attr in info.relations and info.relations[attr].to_many:
                    set_many(instance, attr, value)
                else:
                    setattr(instance, attr, value)
        instance.save()

        return instance
