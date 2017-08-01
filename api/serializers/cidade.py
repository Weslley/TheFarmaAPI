from rest_framework import serializers
from datetime import datetime
from api.models.cidade import Cidade
from api.models.farmacia import Farmacia
from api.models.uf import Uf
from api.serializers.uf import UfSerializer


class CidadeSerializer(serializers.ModelSerializer):
    uf = UfSerializer()
    data_atualizacao = serializers.DateTimeField(format='%s')
    coberta_pelo_thefarma = serializers.SerializerMethodField()

    class Meta:
        model = Cidade
        fields = '__all__'

    def get_coberta_pelo_thefarma(self, obj):
        return True if Farmacia.objects.filter(endereco__cidade=obj).count() > 0 else False


class CidadeBasicSerializer(serializers.ModelSerializer):
    uf = serializers.CharField(source='uf.sigla')

    class Meta:
        model = Cidade
        fields = ('ibge', 'nome', 'uf')
        extra_kwargs = {
            'ibge': {'read_only': True},
        }


class CidadeCreateUpdateSerializer(serializers.Serializer):
    ibge = serializers.IntegerField()
    nome = serializers.CharField(max_length=150, required=False)
    uf = serializers.CharField(max_length=2, required=False)
    uf_nome = serializers.CharField(source='uf.nome', read_only=True)

    def get_object(self, ibge):
        try:
            return Cidade.objects.get(ibge=ibge)
        except Cidade.DoesNotExist:
            return None

    def validate_uf(self, value):
        try:
            return Uf.objects.get(sigla=value)
        except Uf.DoesNotExist:
            return None

    def validate_ibge(self, value):
        obj = self.get_object(value)
        if not obj:
            raise serializers.ValidationError('Cidade não cadastrada.')
        return value

    def validate(self, attrs):
        if 'nome' in attrs and 'uf' not in attrs:
            raise serializers.ValidationError('Nome e UF devem ser inseridos juntos.')

        if 'nome' not in attrs and 'uf' in attrs:
            raise serializers.ValidationError('Nome e UF devem ser inseridos juntos.')

        return attrs

    def create(self, validated_data):
        obj = self.get_object(validated_data['ibge'])
        return obj if obj else Cidade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ibge = validated_data.get('ibge', instance.ibge)
        instance.nome = validated_data.get('nome', instance.nome)
        instance.uf = validated_data.get('uf', instance.uf)
        instance.data_atualizacao = datetime.now()
        instance.save()
        return instance


class CoberturaCidadeSerializer(serializers.ModelSerializer):
    uf = serializers.CharField(source='uf.sigla')
    coberta_pelo_thefarma = serializers.SerializerMethodField()

    class Meta:
        model = Cidade
        fields = ('ibge', 'nome', 'uf', 'coberta_pelo_thefarma')

    def get_coberta_pelo_thefarma(self, obj):
        return True if Farmacia.objects.filter(endereco__cidade=obj).count() > 0 else False
