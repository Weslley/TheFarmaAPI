from rest_framework import serializers

from api.models.post import Post
from api.serializers.user import UserSerializer


class PostExportSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    curtidas = serializers.IntegerField(source='likes')

    class Meta:
        model = Post
        fields = (
            'id',
            'usuario',
            'titulo',
            'imagem',
            'video',
            'conteudo',
            'url_referencia',
            'data_atualizacao',
            'tipo',
            'curtidas'
        )
