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


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def create(self, validated_data):
        email = validated_data['email']
        username = email if len(email) < 150 else email[:149]
        user = User(
            email=email,
            username=username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
