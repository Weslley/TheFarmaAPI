from rest_framework import serializers

from api.models.log import Log


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            "data_criacao": {"read_only": True},
            "data_atualizacao": {"read_only": True},
            "remote_ip": {"read_only": True},
            "browser": {"read_only": True}
        }
