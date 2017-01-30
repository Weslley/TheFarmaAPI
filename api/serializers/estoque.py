from rest_framework import serializers
from api.models.apresentacao import Apresentacao


class EstoqueCreateUpdateSerializer(serializers.Serializer):
    codigo_barras = serializers.IntegerField(min_value=0)
    quantidade = serializers.IntegerField()
    valor = serializers.DecimalField(max_digits=15, decimal_places=2)

    def validate_codigo_barras(self, value):
        """
        Check that the blog post is about Django.
        """
        try:
            apresentacao = Apresentacao.objects.get(codigo_barras=value)
            return apresentacao
        except Apresentacao.DoesNotExist:
            raise serializers.ValidationError('Não existe apresentação com este código de barras')
        except Apresentacao.MultipleObjectsReturned:
            raise serializers.ValidationError('Apresentação com código de barras duplicado.')
        except Exception as err:
            raise serializers.ValidationError(str(err))

    def create(self, validated_data):
        return dict(validated_data)

    def update(self, instance, validated_data):
        instance['codigo_barras'] = validated_data.get('codigo_barras', instance['codigo_barras'])
        instance['quantidade'] = validated_data.get('quantidade', instance['quantidade'])
        instance['valor'] = validated_data.get('valor', instance['valor'])
        return instance
