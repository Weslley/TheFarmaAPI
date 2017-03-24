from django.contrib.auth.models import User
from rest_framework import serializers


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


class DefaultUserSerializer(serializers.Serializer):
    nome = serializers.CharField()
    sobrenome = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    senha = serializers.CharField(max_length=30, style={'input_type': 'password'})
    confirmacao_senha = serializers.CharField(max_length=30, style={'input_type': 'password'})

    def validate_senha(self, value):
        confirmacao = self.initial_data['confirmacao_senha']
        confirmacao = confirmacao.strip()

        if value != confirmacao:
            raise serializers.ValidationError("As senhas não conferem !")

        return value

    def create(self, validated_data):
        # return Comment.objects.create(**validated_data)
        nome = validated_data['nome']
        sobrenome = validated_data['sobrenome'] if 'sobrenome' in validated_data else ''
        email = validated_data['email']
        senha = validated_data['senha']
        username = nome[:6].ljust(10, 'a') + email[:40].ljust(60, '2')
        usuario = User.objects.create_user(username, email, senha)
        usuario.first_name = nome
        usuario.last_name = sobrenome
        usuario.save()

        return usuario

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('nome', instance.content)
        instance.last_name = validated_data.get('sobrenome', instance.created)
        instance.save()
        return instance
