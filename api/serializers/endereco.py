import traceback

from rest_framework import serializers
from rest_framework.compat import set_many
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import as_serializer_error, empty
from rest_framework.utils import model_meta

from api.models.bairro import Bairro
from api.models.cidade import Cidade
from api.models.endereco import Endereco
from api.serializers.bairro import BairroCreateUpdateSerializer
from api.serializers.cidade import CidadeCreateUpdateSerializer


class EnderecoSerializer(serializers.ModelSerializer):
    cidade = CidadeCreateUpdateSerializer()
    bairro = BairroCreateUpdateSerializer()

    def validate_cidade(self, value):
        cidade = Cidade.objects.get(ibge=value['ibge'])
        return cidade

    def validate_bairro(self, value):
        bairro = Bairro.objects.get(id=value['id'])
        return bairro

    class Meta:
        model = Endereco
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'data_atualizacao': {'read_only': True},
        }

    def create(self, validated_data):
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                set_many(instance, field_name, value)

        return instance
