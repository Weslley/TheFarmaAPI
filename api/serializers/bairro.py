from rest_framework import serializers
from api.models.bairro import Bairro
from api.serializers.cidade import CidadeBasicSerializer
from datetime import datetime


class BairroListSerializer(serializers.ModelSerializer):
    cidade = CidadeBasicSerializer()
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Bairro
        fields = '__all__'


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ('id', 'nome')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class BairroCreateUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    nome = serializers.CharField(max_length=60, allow_null=True, required=False)

    def get_object(self, pk):
        try:
            return Bairro.objects.get(id=pk)
        except Bairro.DoesNotExist:
            return None

    def validate_id(self, value):
        try:
            Bairro.objects.get(id=value)
            return value
        except Bairro.DoesNotExist:
            raise serializers.ValidationError('Id de bairro não cadastrado.')

    def create(self, validated_data):
        obj = self.get_object(validated_data['id'])
        return obj

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.data_atualizacao = datetime.now()
        instance.save()
        return instance