from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models.cliente import Cliente
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.db import transaction
import re
from thefarmaapi.backends import EmailModelBackend, FarmaciaBackend


class CreateUserClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=11, required=False, write_only=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    cpf = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'id', 'token', 'cpf')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [UniqueValidator(
                    queryset=User.objects.exclude(representante_farmacia__isnull=False),
                    message='Usuário ja cadastrado com este email.'
                )]
            }
        }

    def validate_cpf(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Número de celular inválido.')

        try:
            User.objects.get(cliente__cpf=data)
            raise serializers.ValidationError('Usuário ja cadastrado com este CPF.')
        except User.DoesNotExist:
            pass

        return data

    def validate_phone(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Número de celular inválido.')

        try:
            User.objects.get(cliente__celular=data)
            raise serializers.ValidationError('Usuário ja cadastrado com este celular.')
        except User.DoesNotExist:
            pass

        return data

    def validate(self, attrs):
        attrs['username'] = self.create_username(attrs['email'])
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            phone = None
            if 'phone' in validated_data:
                phone = validated_data.pop('phone')

            cpf = validated_data.pop('cpf')

            user = super(CreateUserClienteSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            Cliente.objects.create(usuario=user, celular=phone, cpf=cpf)
            Token.objects.create(user=user)
            return user

    def create_username(self, email):
        highest_user_id = User.objects.all().order_by('-id')[0].id  # or something more efficient
        leading_part_of_email = email.split('@', 1)[0]
        leading_part_of_email = re.sub(r'[^a-zA-Z0-9+]', '', leading_part_of_email)  # remove non-alphanumerics
        truncated_part_of_email = leading_part_of_email[:3] + leading_part_of_email[-3:]
        derived_username = '%s%s' % (truncated_part_of_email, highest_user_id + 1)
        return derived_username

from api.models.cliente import Cliente


class UserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='get_full_name')
    foto = serializers.SerializerMethodField('get_foto_url')

    def get_foto_url(self, obj):
        if hasattr(obj, 'cliente'):
            if obj.cliente.foto:
                return 'http://thefarmaapi.herokuapp.com{}'.format(obj.cliente.foto.url)
        return ''

    class Meta:
        model = User
        fields = ('email', 'foto', 'nome')


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, write_only=True)
    email_telefone = serializers.CharField(max_length=254)

    def create(self, validated_data):
        data = {'email_telefone': '', 'password': ''}
        for key in validated_data:
            data[key] = validated_data[key]
        return data

    def update(self, instance, validated_data):
        instance['email_telefone'] = validated_data.get('email_telefone', instance['email_telefone'])
        instance['password'] = validated_data.get('password', instance['password'])
        return instance


# class LoginFacebookSerializer(serializers.Serializer):
#     facebook_id = serializers.CharField(max_length=255, write_only=True)
#
#     def create(self, validated_data):
#         data = {'facebook_id': ''}
#         for key in validated_data:
#             data[key] = validated_data[key]
#         return data
#
#     def update(self, instance, validated_data):
#         instance['facebook_id'] = validated_data.get('facebook_id', instance['facebook_id'])
#         return instance

class LoginFacebookSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name')
    sobrenome = serializers.CharField(source='last_name', required=False)
    facebook_id = serializers.CharField(required=True, source='cliente.facebook_id')
    email = serializers.EmailField(required=True)
    data_nascimento = serializers.DateField(source='cliente.data_nascimento', required=False)
    sexo = serializers.CharField(max_length=1, source='cliente.sexo', required=False)
    foto = serializers.URLField(source='cliente.foto', required=False)

    class Meta:
        model = User
        fields = ('nome', 'sobrenome', 'facebook_id', 'data_nascimento', 'email', 'foto', 'sexo')


class LoginDefautSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    email = serializers.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'password', 'id', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {
                'required': True,
                'allow_blank': False
            }
        }

    def validate_email(self, value):
        if '@' in value:  # se tiver @ no nome do usuário  username vai ser o email
            kwargs = {'email': value}
        elif len(value) <= 11 and value.isdigit():
            kwargs = {'cliente__celular': value}
        elif len(value) > 11 and value.isdigit():
            raise serializers.ValidationError('Certifique-se de que este campo não tenha mais de 11 caracteres.')
        elif len(value) > 11 and not value.isdigit():
            raise serializers.ValidationError('Insira um endereço de email válido.')
        else:
            raise serializers.ValidationError('Este campo é obrigatório.')
        try:
            User.objects.exclude(representante_farmacia__isnull=False).get(**kwargs)
        except User.DoesNotExist:
            if 'email' in kwargs:
                raise serializers.ValidationError('Email não cadastrado.')
            else:
                raise serializers.ValidationError('Celular não cadastrado.')

        return value

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        back = EmailModelBackend()
        self.user = back.authenticate(email, password)

        if not self.user:
            raise serializers.ValidationError('Email ou senha incorretos.')

        return attrs

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(user=self.user)
        if not created:
            token.delete()
            Token.objects.create(user=self.user)
        return self.user

    def update(self, instance, validated_data):
        return instance


class LoginFarmaciaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    email = serializers.EmailField()


    class Meta:
        model = User
        fields = ('email', 'password', 'id', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {
                'required': True,
                'allow_blank': False
            }
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Este campo é obrigatório.')
        try:
            User.objects.exclude(cliente__isnull=False).get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email não cadastrado.')

        return value

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        back = FarmaciaBackend()
        self.user = back.authenticate(email, password)

        if not self.user:
            raise serializers.ValidationError('Email ou senha incorretos.')

        return attrs

    def create(self, validated_data):
        return self.user

    def update(self, instance, validated_data):
        return instance


class DetailUserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name')
    sobrenome = serializers.CharField(source='last_name')
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = User
        fields = ('id', 'nome', 'sobrenome', 'email', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'email': {'read_only': True},
        }
