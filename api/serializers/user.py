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
