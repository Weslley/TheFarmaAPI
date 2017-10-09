from rest_framework import serializers

from api.models.log import Log


class LogSerializer(serializers.ModelSerializer):
    data_criacao = serializers.SerializerMethodField()
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            "data_criacao": {"read_only": True},
            "data_atualizacao": {"read_only": True},
            "remote_ip": {"read_only": True},
            "browser": {"read_only": True}
        }

    def get_data_criacao(self, obj):
        return int(obj.data_criacao.timestamp() * 1000)

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)