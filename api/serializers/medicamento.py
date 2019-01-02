from rest_framework import serializers
from api.models.pedido import ItemPedido

class MedicamentoRelatorio(serializers.ModelSerializer):

    fabricante = serializers.SerializerMethodField()
    codigo_barras = serializers.SerializerMethodField()
    valor_liquido = serializers.SerializerMethodField()
    valor_bruto = serializers.SerializerMethodField()
    nome_produto = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = (
            'id',
            'codigo_barras',
            'fabricante',
            'quantidade',
            'valor_liquido',
            'valor_bruto',
            'nome_produto'
        )
    
    def get_nome_produto(self,obj):
        return obj.apresentacao.produto.nome

    def get_fabricante(self,obj):
        return obj.apresentacao.produto.laboratorio.nome

    def get_codigo_barras(self,obj):
        return obj.apresentacao.codigo_barras
    
    def get_valor_liquido(self,obj):
        return 'R$ {}'.format(obj.total_liquido)

    def get_valor_bruto(self,obj):
        return 'R$ {}'.format(obj.total_bruto)