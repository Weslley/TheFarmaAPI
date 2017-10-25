from django.core.exceptions import ValidationError as DjangoValidationError
from pycards import CreditCard
from rest_framework import serializers
from rest_framework.compat import set_many
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import as_serializer_error, empty
from rest_framework.utils import model_meta
from api.servico_pagamento.servicos.cielo import ServicoCielo
from api.models.cartao import Cartao


class CartaoSerializer(serializers.ModelSerializer):
    numero_cartao = serializers.CharField(max_length=16)

    class Meta:
        model = Cartao
        exclude = ('cliente', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'bandeira': {'allow_blank': True, 'allow_null': True, 'required': False},
            'cvv': {'write_only': True}
        }

    def validate(self, attrs):
        self.card = CreditCard(
            number=attrs['numero_cartao'],
            code=attrs['cvv'],
            cardholder=attrs['nome_proprietario'],
            expire_month=attrs['mes_expiracao'],
            expire_year=attrs['ano_expiracao']
        )
        # if not self.card.is_valid:
        #     raise ValidationError('Cartão inválido.')
        #
        # if self.card.is_expired:
        #     raise ValidationError('Cartão expirado.')

        request = self.context['request']
        # attrs['bandeira'] = self.card.brand
        attrs['bandeira'] = 'Master'
        attrs['cliente'] = request.user.cliente
        attrs['token'] = ServicoCielo.create_token(attrs)
        attrs['numero_cartao'] = attrs['numero_cartao'][-4:]
        return attrs

    def create(self, validated_data):
        try:
            instance = Cartao.objects.create(**validated_data)
        except Exception as err:
            print(type(err))
            print(err)
            raise err

        return instance

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance
