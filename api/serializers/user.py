from django.contrib.auth.models import User
from rest_framework import serializers

from api.models.cliente import Cliente


class UserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='get_full_name')
    foto = serializers.SerializerMethodField('get_foto_url')

    def get_foto_url(self, obj):
        base = ''
        if hasattr(obj, 'cliente'):
            if obj.cliente.foto:
                return 'http://thefarmaapi.herokuapp.com{}'.format(obj.cliente.foto.url)
        return ''

    class Meta:
        model = User
        fields = ('email', 'foto', 'nome')


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, write_only=True)
    email = serializers.CharField(max_length=254)

    def create(self, validated_data):
        data = {'email': '', 'password': ''}
        for key in validated_data:
            data[key] = validated_data[key]
        return data

    def update(self, instance, validated_data):
        instance['email'] = validated_data.get('email', instance['emai'])
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


class CreateUserSerializer(serializers.ModelSerializer):
    telefone = serializers.CharField(max_length=11, required=False, allow_blank=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'telefone')
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value.strip()).count():
            raise serializers.ValidationError('Um usuário com este email já existe.')
        return value

    def validate_telefone(self, value):
        if value and Cliente.objects.filter(telefone=value.strip()).count():
            raise serializers.ValidationError('Um usuário com este telefone já existe.')
        return value

    def create(self, validated_data):
        username = validated_data['telefone'] if 'telefone' in validated_data else None
        email = validated_data['email']

        if not username:
            username = email[:150]

        user = User(
            email=email,
            username=username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DetailUserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name')
    sobrenome = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('id', 'username', 'nome', 'sobrenome', 'email')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'email': {'read_only': True},
        }
