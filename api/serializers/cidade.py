from rest_framework import serializers

from api.models.cidade import Cidade
from api.models.farmacia import Farmacia
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


class CoberturaCidadeSerializer(serializers.ModelSerializer):
    uf = serializers.CharField(source='uf.sigla')
    coberta_pelo_thefarma = serializers.SerializerMethodField()

    class Meta:
        model = Cidade
        fields = ('ibge', 'nome', 'uf', 'coberta_pelo_thefarma')

    def get_coberta_pelo_thefarma(self, obj):
        return True if Farmacia.objects.filter(endereco__cidade=obj).count() > 0 else False
