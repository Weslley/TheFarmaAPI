from django.db import transaction
from rest_framework import serializers

from api.models.cidade import Cidade

from api.models.representante_legal import RepresentanteLegal
from api.serializers.endereco import EnderecoSerializer, EnderecoFarmaciaSerializer
from api.serializers.farmacia import FarmaciaRepresentanteSerializer
from api.serializers.user import RepresentanteUserSerializer


class RepresentanteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    farmacia = FarmaciaRepresentanteSerializer()
    usuario = RepresentanteUserSerializer()

    class Meta:
        model = RepresentanteLegal
        exclude = ('id',)

    def update(self, instance, validated_data):
        with transaction.atomic():

            if 'endereco' in validated_data:
                validated_data.pop('endereco')

            if 'farmacia' in validated_data:
                farmacia_data = validated_data.pop('farmacia')
                serializer = FarmaciaRepresentanteSerializer(
                    instance.farmacia,
                    farmacia_data,
                    **{'context': {'request': self.context['request']}},
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            if 'usuario' in validated_data:
                usuario_data = validated_data.pop('usuario')
                serializer = RepresentanteUserSerializer(
                    instance.usuario,
                    usuario_data,
                    **{
                        'context': {
                            'request': self.context['request'],
                            'view': self.context['view']
                        }
                    },
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return super(RepresentanteSerializer, self).update(instance, validated_data)

class RepresentanteFarmaciaSerializer(serializers.ModelSerializer):
    endereco = EnderecoFarmaciaSerializer()
    usuario = RepresentanteUserSerializer()

    class Meta:
        model = RepresentanteLegal
        fields = '__all__'

    def update(self, instance, validated_data):
        with transaction.atomic():

            if 'endereco' in validated_data:
                endereco_data = validated_data.pop('endereco')
                cidade = endereco_data.pop('cidade')
                endereco_data.update({'cidade': cidade.ibge})
                serializer = EnderecoFarmaciaSerializer(
                    instance.endereco,
                    endereco_data,
                    **{
                        'context': {
                            'request': self.context['request'],
                            'view': self.context['view']
                        }
                    },
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            if 'usuario' in validated_data:
                usuario_data = validated_data.pop('usuario')
                serializer = RepresentanteUserSerializer(
                    instance.usuario,
                    usuario_data,
                    **{
                        'context': {
                            'request': self.context['request'],
                            'view': self.context['view']
                        }
                    },
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return super(RepresentanteFarmaciaSerializer, self).update(instance, validated_data)
