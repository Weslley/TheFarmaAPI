from rest_framework import serializers
from api.models.apresentacao import Apresentacao
from api.serializers.tabela_preco import TabelaPrecoSerializer


class ApresentacaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apresentacao
        fields = ('nome', 'id')


class ApresentacaoSerializer(serializers.ModelSerializer):
    tabelas = TabelaPrecoSerializer(many=True)

    class Meta:
        model = Apresentacao
        fields = ('codigo_barras', 'nome', 'registro_ms', 'imagem', 'tabelas')


class ApresentacaoExportSerializer(serializers.ModelSerializer):
    tabelas = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Apresentacao
        fields = '__all__'
