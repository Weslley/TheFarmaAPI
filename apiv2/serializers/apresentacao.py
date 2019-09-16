from rest_framework import serializers

from api.models.apresentacao import Apresentacao
from api.serializers.apresentacao import ProdutoSimplesSerializer

class ApresentacaoPropostaItemSerializer(serializers.ModelSerializer):
    produto = ProdutoSimplesSerializer()
    imagem = serializers.SerializerMethodField()

    class Meta:
        model = Apresentacao
        fields = ('id', 'nome', 'imagem', 'produto', 'codigo_barras')

    def get_imagem(self, obj):
        return obj.imagem_url