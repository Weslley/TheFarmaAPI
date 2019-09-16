from rest_framework import serializers

from api.models.produto import Produto
from api.serializers.apresentacao import (ApresentacaoBusca, ApresentacaoListSerializer)
from api.serializers.principio_ativo import PrincipioAtivoBasicSerializer


class MedicamentoSerializer(serializers.ModelSerializer):
    apresentacoes = ApresentacaoListSerializer(many=True)
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class MedicamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('nome', 'id')


class MedicamentoExportSerializer(serializers.ModelSerializer):
    apresentacoes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    data_atualizacao = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'

    def get_data_atualizacao(self, obj):
        return int(obj.data_atualizacao.timestamp() * 1000)


class ProdutoSerializer(serializers.ModelSerializer):
    apresentacoes = serializers.SerializerMethodField()
    fabricante = serializers.CharField(read_only=True, source='laboratorio.nome')
    principio_ativo = PrincipioAtivoBasicSerializer()

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'tipo', 'fabricante', 'apresentacoes', 'principio_ativo')

    def get_apresentacoes(self, obj):
        qs = obj.apresentacoes.filter(ativo=True)
        serializer = ApresentacaoBusca(instance=qs, many=True, context=self.context)
        return serializer.data


class ProdutoNovoSerializer(serializers.ModelSerializer):
    ids = serializers.SerializerMethodField()
    nome = serializers.CharField()
    tipo_venda = serializers.SerializerMethodField() 

    class Meta:
        model = Produto
        fields = ('ids', 'nome', 'tipo_venda')

    def get_ids(self, obj):
        qs = Produto.objects.filter(apresentacoes__isnull=False, nome__iexact=obj['nome']).distinct()
        return [p['id'] for p in qs.values('id')]

    def get_tipo_venda(self, obj):
        try:
            qs = Produto.objects.filter(apresentacoes__isnull=False, nome__iexact=obj['nome']).distinct().first()
            return qs.principio_ativo.tipo_venda
        except Exception as err:
            print(str(err))
            return 0

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')


class ProdutoIndicadorVendaSerializer(serializers.ModelSerializer):
    principio_ativo = serializers.CharField(source='principio_ativo.nome')
    laboratorio = serializers.CharField(source='laboratorio.nome')
    vendas = serializers.IntegerField()

    class Meta:
        model = Produto
        fields = ('nome', 'vendas', 'principio_ativo', 'laboratorio')