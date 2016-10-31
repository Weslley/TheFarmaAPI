from rest_framework import serializers
from api.models.apresentacao import Apresentacao
from api.serializers.tabela_preco import TabelaPrecoSerializer


class ApresentacaoListSerializer(serializers.HyperlinkedModelSerializer):
    pmc = serializers.DecimalField(max_digits=15, decimal_places=2, source='tabela.pmc')
    apresentacao = serializers.HyperlinkedIdentityField(view_name='apresentacao-view', lookup_field='id', format='html')

    class Meta:
        model = Apresentacao
        fields = ('nome', 'pmc', 'apresentacao')


class ApresentacaoSerializer(serializers.ModelSerializer):
    tabelas = TabelaPrecoSerializer()

    class Meta:
        model = Apresentacao
        fields = ('codigo_barras', 'nome', 'registro_ms', 'imagem', 'tabelas')
