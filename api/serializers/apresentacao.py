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
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)
