import re

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator
from datetime import datetime
from api.models.cliente import Cliente
from api.tasks.cliente import update_foto_facebook
from api.utils import sexo
from thefarmaapi.backends import EmailModelBackend, FarmaciaBackend
from api.models.enums.login_type import LoginType
from api.utils import sms_code
from api.utils.generics import create_username, create_email

import base64
import six
import uuid
import imghdr


class LoginClienteSerializer(serializers.ModelSerializer):
    login_type = serializers.ChoiceField(choices=LoginType.choices(), write_only=True, required=True)
    email = serializers.EmailField(max_length=250, required=False, write_only=True)
    password = serializers.CharField(required=False, write_only=True)
    facebook_id = serializers.IntegerField(required=False, write_only=True)
    celular = serializers.IntegerField(required=False, write_only=True)
    codigo_sms = serializers.IntegerField(required=False, write_only=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    fcm = serializers.CharField(required=False)
    user_queryset = User.objects.exclude(representante_farmacia__isnull=False, cliente__isnull=False)

    class Meta:
        model = User
        fields = (
            'login_type',
            'email',
            'password',
            'facebook_id',
            'celular',
            'codigo_sms',
            'token',
            'fcm',
        )

    def validate_login_type(self, data):
        if data == LoginType.EMAIL:
            if 'email' not in self.initial_data:
                raise serializers.ValidationError('Email é obrigatório.')
            if 'password' not in self.initial_data:
                raise serializers.ValidationError('Senha é obrigatória.')
        elif data == LoginType.FACEBOOK:
            if 'facebook_id' not in self.initial_data:
                raise serializers.ValidationError('Facebook é obrigatório.')
        else:
            if 'celular' not in self.initial_data:
                raise serializers.ValidationError('Celular é obrigatório.')

        return data

    def validate_email(self, data):
        if data:
            try:
                user = self.user_queryset.get(email=data)
                if not hasattr(user, 'cliente'):
                    raise serializers.ValidationError('Email já utilizado')
            except:
                pass
            
        return data

    def validate_password(self, data):    
        if 'login_type' not in self.initial_data:
            return None
        if self.initial_data['login_type'] == LoginType.EMAIL:
            email = self.initial_data['email']
            try:
                user = self.user_queryset.get(email=email)
                if not user.check_password(data):
                    raise serializers.ValidationError('Senha incorreta.')
            except User.DoesNotExist:
                pass

        return data

    def validate_celular(self, data):
        if not self.user_queryset.filter(cliente__celular=data).exists():
            user = User.objects.create(username=create_username(create_email(data)))
            Cliente.objects.create(usuario=user, celular=data)

            # Enviando SMS
            sms_code.send_sms_code(user)
            raise serializers.ValidationError('Enviamos um código via SMS.')

        return data

    def validate_codigo_sms(self, data):
        celular = self.initial_data['celular']
        user = self.user_queryset.get(cliente__celular=celular)

        if not sms_code.check_code(user, data):
            raise serializers.ValidationError('Código SMS inválido.')

        return data

    def validate_facebook_id(self, data):
        if self.initial_data['login_type'] == LoginType.FACEBOOK:
            try:
                self.user_queryset.get(cliente__facebook_id=data)
            except User.DoesNotExist:
                if 'email' not in self.initial_data:
                    raise serializers.ValidationError('Email é obrigatório.')
        return data

    def validate(self, validated_data):
        if validated_data['login_type'] == LoginType.CELULAR:
            if 'codigo_sms' not in validated_data or ('codigo_sms' in validated_data and not validated_data['codigo_sms']):
                if self.user_queryset.filter(cliente__celular=validated_data['celular']).exists():
                    user = self.user_queryset.get(cliente__celular=validated_data['celular'])
                    sms_code.send_sms_code(user)  # Enviando SMS
                raise serializers.ValidationError('Código SMS é obrigatório.')
        elif validated_data['login_type'] == LoginType.FACEBOOK:
            if 'email' in validated_data and validated_data['email']:
                exist_user = self.user_queryset.filter(email=validated_data['email'], cliente__facebook_id__isnull=False).exists()
                if exist_user:
                    user = self.user_queryset.get(email=validated_data['email'], cliente__facebook_id__isnull=False)
                    if user.cliente.facebook_id != validated_data['facebook_id']:
                        raise serializers.ValidationError('Facebook token inválido.')
            else:
                exist_user = self.user_queryset.filter(cliente__facebook_id=validated_data['facebook_id']).exists()
                if exist_user:
                    user = self.user_queryset.get(cliente__facebook_id=validated_data['facebook_id'])
                    if not user.email:
                        raise serializers.ValidationError('Email é obrigatório.')

        return validated_data

    def login_email(self, email, password):
        user, created = self.user_queryset.get_or_create(email=email)
        if created:
            Cliente.objects.create(usuario=user)
            user.username = create_username(email)
            user.set_password(password)
            user.save()

        return user

    def login_facebook(self, facebook_id, email=None):
        if email:
            try:
                exist_user = self.user_queryset.filter(email=email).exists()
                if exist_user:
                    exist_user = self.user_queryset.filter(email=email, cliente__facebook_id__isnull=True).exists()
                    if exist_user:
                        user = self.user_queryset.get(email=email, cliente__facebook_id__isnull=True)
                        if not hasattr(user, 'cliente'):
                            Cliente.objects.create(usuario=user, facebook_id=facebook_id)
                        user.cliente.facebook_id = facebook_id
                        user.cliente.save()
                    else:
                        exist_user = self.user_queryset.filter(email=email, cliente__facebook_id__isnull=False).exists()
                        if exist_user:
                            user = self.user_queryset.get(email=email, cliente__facebook_id__isnull=False)
                            assert user.cliente.facebook_id != facebook_id, ('Tokens inválidos.')
                else:
                    user = self.user_queryset.get(cliente__facebook_id=facebook_id)
                    user.email = email
                    user.save()
            except User.DoesNotExist:
                data = self._kwargs.get('data')
                fb_data = data.get('facebook_data')
                foto_url = fb_data.get('picture').get('data').get('url')

                user = User.objects.create(email=email)
                user.username = create_username(email)
                user.first_name = fb_data.get('first_name')
                user.last_name = fb_data.get('last_name')
                user.save()

                cliente = Cliente.objects.create(
                    usuario=user,
                    facebook_id=data.get('facebook_id')
                )
                update_foto_facebook.apply_async(
                    [cliente.id, foto_url], 
                    queue='update_cliente', countdown=1
                )

            return user
        else:
            exist_user = self.user_queryset.filter(cliente__facebook_id=facebook_id).exists()

            if exist_user:
                return self.user_queryset.get(cliente__facebook_id=facebook_id)

            assert email is not None, ('Email não poder ser nulo ao criar cliente novo com facebook')

    def login_celular(self, celular):
        user = self.user_queryset.get(cliente__celular=celular)
        user.cliente.celular_confirmado = True
        user.cliente.save()
        return user

    def create(self, validated_data):
        with transaction.atomic():
            login_type = validated_data['login_type']
            if login_type == LoginType.EMAIL:
                user = self.login_email(validated_data['email'], validated_data['password'])
            elif login_type == LoginType.FACEBOOK:
                user = self.login_facebook(validated_data['facebook_id'], validated_data.get('email', None))
            else:
                user = self.login_celular(validated_data['celular'])

            user.last_login = datetime.now()
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            #verifica se mandou o fcm token
            fcm = validated_data.pop('fcm',None)
            if fcm:
                cliente = Cliente.objects.get(usuario_id=user.id)
                cliente.fcm_token = fcm
                cliente.save()
            if not created:
                token.delete()
                Token.objects.create(user=user)
            
            return user


class EnviarCodigoSmsSerializer(serializers.ModelSerializer):
    celular = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = User
        fields = ('celular', )

    def validate_celular(self, data):
        if not data.isdigit():
            raise serializers.ValidationError('Número de celular inválido.')

        return data

    def create(self, validated_data):
        with transaction.atomic():
            try:
                user = User.objects.get(cliente__celular=validated_data['celular'])
            except User.DoesNotExist:
                user = User.objects.create(username=create_username(create_email(validated_data['celular'])))
                Cliente.objects.create(usuario=user, celular=validated_data['celular'])

            # Enviando SMS
            sms_code.send_sms_code(user)

            return user


class ImageB64Field(serializers.ImageField):
    # Converte b64 em imagem

    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "{0}.{1}".format(file_name, file_extension)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(ImageB64Field, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

        # extension = imghdr.what(file_name, decoded_file)
        extension = "jpg"

        return extension


class CreateUserClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    celular = serializers.CharField(max_length=11, required=False, write_only=True, allow_null=True, allow_blank=True)
    token = serializers.CharField(max_length=250, read_only=True, source='auth_token.key')
    cpf = serializers.CharField(max_length=11, write_only=True, required=False)
    sexo = serializers.ChoiceField(choices=sexo.CHOICES, required=False, allow_blank=True, allow_null=True)
    foto = ImageB64Field(max_length=None, use_url=True, required=False, allow_empty_file=True)
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
            raise serializers.ValidationError('Número do CPF inválido.')

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
        attrs['username'] = create_username(attrs['email'])
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            cliente_kwargs = {}
            user_kwargs = {}
            foto = None

            user_fields = ['nome', 'sobrenome']
            cliente_fields = [
                'celular', 'cpf', 'sexo', 
                'facebook_id', 'data_nascimento', 'foto'
            ]

            # if 'foto' in validated_data:
            #     foto = validated_data.pop('foto')

            for key in user_fields:
                if key in validated_data:
                    user_kwargs[key] = validated_data.pop(key)

            for key in cliente_fields:
                if key in validated_data:
                    cliente_kwargs[key] = validated_data.pop(key)

            user = super(CreateUserClienteSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.first_name = user_kwargs['nome'] if 'nome' in user_kwargs else ''
            user.last_name = user_kwargs['sobrenome'] if 'sobrenome' in user_kwargs else ''
            user.save()
            cliente = Cliente.objects.create(usuario=user, **cliente_kwargs)
            if cliente.celular:
                pass  # enviar sms
            Token.objects.create(user=user)

            # if foto:
            #     update_foto_facebook.apply_async([cliente.id, foto], queue='update_cliente', countdown=1)

            return user


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
    celular = serializers.IntegerField(required=False)

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


class LoginCelularSerializer(serializers.ModelSerializer):
    pass


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
    nome = serializers.SerializerMethodField()
    sobrenome = serializers.CharField(source='last_name')
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = User
        fields = ('id', 'nome', 'sobrenome', 'email', 'token')
        extra_kwargs = {
            'email': {'read_only': True},
            'id': {'read_only': True},
        } 


class DetailUserNoTokenSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name')
    sobrenome = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('nome', 'sobrenome', 'email')
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
