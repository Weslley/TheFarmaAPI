import re

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from api.models.cliente import Cliente
from api.tasks.cliente import update_foto_facebook
from api.utils import sexo
from thefarmaapi.backends import EmailModelBackend, FarmaciaBackend


class CreateUserClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    celular = serializers.CharField(max_length=11, required=False, write_only=True, allow_null=True, allow_blank=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    cpf = serializers.CharField(max_length=11, write_only=True)
    sexo = serializers.ChoiceField(choices=sexo.CHOICES, required=False, allow_blank=True, allow_null=True)
    foto = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    facebook_id = serializers.IntegerField(required=False, allow_null=True)
    nome = serializers.CharField(max_length=30, required=False, allow_blank=True)
    sobrenome = serializers.CharField(max_length=30, required=False, allow_blank=True)
    data_nascimento = serializers.DateField(required=False, allow_null=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y'])

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'celular',
            'id',
            'token',
            'cpf',
            'sexo',
            'foto',
            'facebook_id',
            'data_nascimento',
            'nome',
            'sobrenome'
        )
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

    def validate_celular(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Número de celular inválido.')

        try:
            User.objects.get(cliente__celular=data)
            raise serializers.ValidationError('Usuário ja cadastrado com este celular.')
        except User.DoesNotExist:
            pass

        return data

    def validate_facebook_id(self, value):
        try:
            User.objects.exclude(representante_farmacia__isnull=False).get(cliente__facebook_id=value)
            raise serializers.ValidationError('Usuário já cadastrado.')
        except User.DoesNotExist:
            return value

    def validate(self, attrs):
        attrs['username'] = self.create_username(attrs['email'])
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            cliente_kwargs = {}
            user_kwargs = {}
            foto = None

            if 'foto' in validated_data:
                foto = validated_data.pop('foto')

            for key in ['nome', 'sobrenome']:
                if key in validated_data:
                    user_kwargs[key] = validated_data.pop(key)

            for key in ['celular', 'cpf', 'sexo', 'facebook_id', 'data_nascimento']:
                if key in validated_data:
                    cliente_kwargs[key] = validated_data.pop(key)

            user = super(CreateUserClienteSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.first_name = user_kwargs['nome'] if 'nome' in user_kwargs else ''
            user.last_name = user_kwargs['sobrenome'] if 'sobrenome' in user_kwargs else ''
            user.save()
            cliente = Cliente.objects.create(usuario=user, **cliente_kwargs)
            Token.objects.create(user=user)

            if foto:
                update_foto_facebook.apply_async([cliente.id, foto], queue='update_cliente', countdown=1)

            return user

    def create_username(self, email):
        highest_user_id = User.objects.all().order_by('-id')[0].id  # or something more efficient
        leading_part_of_email = email.split('@', 1)[0]
        leading_part_of_email = re.sub(r'[^a-zA-Z0-9+]', '', leading_part_of_email)  # remove non-alphanumerics
        truncated_part_of_email = leading_part_of_email[:3] + leading_part_of_email[-3:]
        derived_username = '%s%s' % (truncated_part_of_email, highest_user_id + 1)
        return derived_username


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
    password = serializers.CharField(write_only=True, required=True, allow_blank=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    email = serializers.CharField(max_length=250, required=True, allow_blank=True)
    facebook_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('facebook_id', 'email', 'password', 'id', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate_password(self, value):
        data = self._kwargs['data']

        if 'facebook_id' in data and data['facebook_id']:
            return value
        elif not value:
            raise serializers.ValidationError('Este campo é obrigatório.')

        return value

    def validate_facebook_id(self, value):
        try:
            User.objects.exclude(representante_farmacia__isnull=False).get(cliente__facebook_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuário não cadastrado.')

        return value

    def validate_email(self, value):
        data = self._kwargs['data']

        if 'facebook_id' in data and data['facebook_id']:
            return value

        if '@' in value:  # se tiver @ no nome do usuário  username vai ser o email
            kwargs = {'email': value}
        elif len(value) <= 11 and value.isdigit():
            kwargs = {'cliente__celular': value}
        elif len(value) > 11 and value.isdigit():
            raise serializers.ValidationError('Certifique-se de que este campo não tenha mais de 11 caracteres.')
        elif len(value) > 0 and not value.isdigit():
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
        facebook_id = attrs['facebook_id'] if 'facebook_id' in attrs and attrs['facebook_id'] else None

        if facebook_id:
            self.user = User.objects.exclude(representante_farmacia__isnull=False).get(cliente__facebook_id=facebook_id)
        else:
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
    nome = serializers.CharField(read_only=True, source='first_name')
    farmacia_id = serializers.IntegerField(source='representante_farmacia.farmacia_id', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'id', 'token', 'nome', 'farmacia_id')
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
        fields = ('nome', 'sobrenome', 'email', 'token')
        extra_kwargs = {
            'email': {'read_only': True},
        }


class RepresentanteUserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name', required=False, max_length=30)
    sobrenome = serializers.CharField(source='last_name', required=False, max_length=30)
    token = serializers.CharField(read_only=True, source='auth_token.key')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('nome', 'sobrenome', 'email', 'token', 'password')

    def validate_email(self, value):
        obj = self.context['view'].get_object()

        if not value:
            raise serializers.ValidationError('Este campo é obrigatório.')

        if value == obj.usuario.email:
            return value

        if User.objects.exclude(cliente__isnull=False).filter(email=value).exists():
            raise serializers.ValidationError('Já existe usuário com este email')

        return value

    def run_validation(self, data=empty):
        value = super(RepresentanteUserSerializer, self).run_validation(data)
        if 'first_name' in data:
            value['first_name'] = data['first_name']

        if 'last_name' in data:
            value['last_name'] = data['last_name']
        return value

    def update(self, instance, validated_data):
        instance = super(RepresentanteUserSerializer, self).update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
        return instance
