from django.db import transaction
from rest_framework import serializers

from api.models.farmacia import Farmacia
from api.serializers.conta_bancaria import ContaBancariaSerializer
from datetime import datetime

from api.utils.generics import calcula_distancia


class FarmaciaListSerializer(serializers.ModelSerializer):
    horario_funcionamento = serializers.SerializerMethodField()
    distancia = serializers.SerializerMethodField()

    class Meta:
        model = Farmacia
        fields = (
            'id',
            'cnpj',
            'nome_fantasia',
            'razao_social',
            'tempo_entrega',
            'servico_entregador',
            'horario_funcionamento',
            'distancia'
        )

    def get_distancia(self, obj):
        farmacia = (obj.latitude, obj.longitude)
        cliente = (self.context['pedido'].latitude, self.context['pedido'].longitude)
        if all(farmacia) and all(cliente):
            return round(calcula_distancia(farmacia, cliente), 2)
        return 0

    def get_horario_funcionamento(self, obj):
        print(self)
        return datetime.now().time().strftime('%H:%M:%S')


class FarmaciaSerializer(serializers.ModelSerializer):
    data_atualizacao = serializers.DateTimeField(format='%s')

    class Meta:
        model = Farmacia
        fields = '__all__'


class FarmaciaRepresentanteSerializer(serializers.ModelSerializer):
    conta_bancaria = ContaBancariaSerializer()

    class Meta:
        model = Farmacia
        fields = ('cnpj', 'nome_fantasia', 'razao_social', 'conta_bancaria')

    def update(self, instance, validated_data):
        with transaction.atomic():

            if 'conta_bancaria' in validated_data:
                validated_data.pop('conta_bancaria')
                conta_bancaria_data = self.context['request'].data['farmacia']['conta_bancaria']
                serializer = ContaBancariaSerializer(
                    instance.conta_bancaria,
                    conta_bancaria_data,
                    **{'context': {'request': self.context['request']}},
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return super(FarmaciaRepresentanteSerializer, self).update(instance, validated_data)
