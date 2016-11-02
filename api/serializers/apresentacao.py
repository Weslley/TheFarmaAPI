from rest_framework import serializers
from api.models.apresentacao import Apresentacao
from api.serializers.tabela_preco import TabelaPrecoSerializer


class ApresentacaoListSerializer(serializers.HyperlinkedModelSerializer):
    apresentacao = serializers.HyperlinkedIdentityField(view_name='apresentacao-view', lookup_field='id', format='html')

    class Meta:
        model = Apresentacao
        fields = ('nome', 'apresentacao')


class ApresentacaoSerializer(serializers.ModelSerializer):
    tabelas = TabelaPrecoSerializer(many=True)

    class Meta:
        model = Apresentacao
        fields = ('codigo_barras', 'nome', 'registro_ms', 'imagem', 'tabelas')
