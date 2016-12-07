from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='get_full_name')
    foto = serializers.SerializerMethodField('get_foto_url')

    def get_foto_url(self, obj):
        base = ''
        if hasattr(obj, 'perfil'):
            if obj.perfil.foto:
                return 'http://thefarmaapi.herokuapp.com{}'.format(obj.perfil.foto.url)
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
    sobrenome = serializers.CharField(source='last_name')
    facebook_id = serializers.CharField(required=True, source='perfil.facebook_id')
    email = serializers.EmailField(required=True)
    data_nascimento = serializers.DateField(source='perfil.data_nascimento')
    sexo = serializers.CharField(max_length=1, source='perfil.sexo')
    foto = serializers.URLField(source='perfil.foto')

    class Meta:
        model = User
        fields = ('email', )
