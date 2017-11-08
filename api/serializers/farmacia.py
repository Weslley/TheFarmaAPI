from django.db import transaction
from rest_framework import serializers

from api.models.farmacia import Farmacia
from api.models.feriado import Feriado
from api.serializers.conta_bancaria import ContaBancariaSerializer
from datetime import datetime

from api.serializers.endereco import EnderecoClienteCreateSerializer, EnderecoSerializer
from api.utils.generics import calcula_distancia


class FarmaciaListSerializer(serializers.ModelSerializer):
    horario_funcionamento = serializers.SerializerMethodField()
    distancia = serializers.SerializerMethodField()
    endereco = EnderecoClienteCreateSerializer()
    tempo_entrega = serializers.SerializerMethodField()
    horarios = serializers.SerializerMethodField()

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
            'distancia',
            'endereco',
            'latitude',
            'longitude',
            'horarios',
            'telefone'
        )

    def get_horarios(self, obj):
        dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
        horario_format = '{:%H:%M} até {:%H:%M}'
        horarios = [
            {
                'dia_semana': dia, 'horario': horario_format.format(
                    obj.horario_funcionamento_segunda_sexta_inicial,
                    obj.horario_funcionamento_segunda_sexta_final
                )
            } for dia in dias_semana
        ]
        horarios.append(
            {
                'dia_semana': 'Sábado', 'horario': horario_format.format(
                    obj.horario_funcionamento_sabado_inicial,
                    obj.horario_funcionamento_sabado_final
                )
            }
        )
        horarios.append(
            {
                'dia_semana': 'Domingo', 'horario': horario_format.format(
                    obj.horario_funcionamento_domingo_inicial,
                    obj.horario_funcionamento_domingo_final
                )
            }
        )
        horarios.append(
            {
                'dia_semana': 'Feriado', 'horario': horario_format.format(
                    obj.horario_funcionamento_feriado_inicial,
                    obj.horario_funcionamento_feriado_final
                )
            }
        )
        return horarios

    def get_tempo_entrega(self, obj):
        tempo = int(obj.tempo_entrega.total_seconds())

        if tempo < 60:
            return '{} segundo{}'.format(tempo, 's' if tempo > 1 else '')

        tempo = int(tempo / 60)

        if tempo < 60:
            return '{} minuto{}'.format(tempo, 's' if tempo > 1 else '')

        horas = int(tempo / 60)
        minutos = int(tempo % 60)
        str_minutos = ' e {} minuto{}'.format(minutos, 's' if minutos > 1 else '')
        return '{} hora{}{}'.format(horas, 's' if horas > 1 else '', str_minutos if minutos > 0 else '')

    def get_distancia(self, obj):
        farmacia = (obj.latitude, obj.longitude)
        cliente = (self.context['pedido'].latitude, self.context['pedido'].longitude)
        if all(farmacia) and all(cliente):
            distancia = round(calcula_distancia(farmacia, cliente), 2)
        else:
            distancia = 0

        if distancia == 0:
            return '0m'
        if distancia >= 1:
            return '{distancia}km'.format(distancia=distancia)
        else:
            return '{distancia}m'.format(distancia=distancia * 1000)

    def get_horario_funcionamento(self, obj):
        hoje = datetime.now()

        # Feriado nacional
        if Feriado.objects.filter(dia=hoje.day, mes=hoje.month, uf__isnull=True).exists():
            return obj.horario_funcionamento_feriado_final.strftime('%H:%M')

        # Feriado estadual
        if Feriado.objects.filter(dia=hoje.day, mes=hoje.month, uf=obj.endereco.cidade.uf).exists():
            return obj.horario_funcionamento_feriado_final.strftime('%H:%M')

        # Domingo
        if hoje.weekday() == 6:
            return obj.horario_funcionamento_domingo_final.strftime('%H:%M')

        # Sabado
        if hoje.weekday() == 5:
            return obj.horario_funcionamento_sabado_final.strftime('%H:%M')

        # Segunda a sexta
        return obj.horario_funcionamento_segunda_sexta_final.strftime('%H:%M')


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


class FarmaciaEnderecoSerializer(FarmaciaListSerializer):
    endereco = EnderecoSerializer()
