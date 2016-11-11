from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='get_full_name')
    foto = serializers.ImageField(source='perfil.foto')

    class Meta:
        model = User
        fields = ('email', 'foto', 'nome')
