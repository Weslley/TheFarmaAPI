from rest_framework import serializers
from datetime import datetime
from api.models.notificacao import Notificacao


class NotificacaoSerializer(serializers.ModelSerializer):
    mensagem = serializers.SerializerMethodField()

    class Meta:
        model = Notificacao
        exclude = ('cliente', )
    
    def get_mensagem(self,obj):
        msg = ''
        if obj.mensagem_extra:
            msg = obj.mensagem_extra
            #verifica se precisa formatar a saida
            if '{}' in msg:
                msg = msg.format(obj.id)
        return msg

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