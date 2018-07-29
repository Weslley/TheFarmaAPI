from rest_framework import serializers
from datetime import datetime
from api.models.notificacao import Notificacao


class NotificacaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notificacao
        exclude = ('cliente', )


class NotificacaoUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notificacao
        exclude = ('cliente', )
        extra_kwargs = {
            'id': {'read_only': True},
            'tipo': {'read_only': True},
            'titulo': {'read_only': True},
            'mensagem': {'read_only': True},
            'data_criacao': {'read_only': True},
            'data_atualizacao': {'read_only': True},
            'data': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance = super(NotificacaoUpdateSerializer, self).update(instance, validated_data)
        instance.data_atualizacao = datetime.now()
        instance.save()
        return instance