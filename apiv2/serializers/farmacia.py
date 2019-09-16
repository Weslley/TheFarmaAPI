from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from api.models.feriado import Feriado
from api.models.farmacia import Farmacia

from api.utils.generics import calcula_distancia

from apiv2.serializers.endereco import EnderecoFarmaciaSerializer

class FarmaciaPedidoSerializer(serializers.ModelSerializer):
    distancia = serializers.SerializerMethodField()
    endereco = EnderecoFarmaciaSerializer()
    tempo_entrega = serializers.SerializerMethodField()
    horario_funcionamento = serializers.SerializerMethodField()

    class Meta:
        model = Farmacia
        fields = (
            'id',
            'cnpj',
            'valor_frete',
            'nome_fantasia',
            'tempo_entrega',
            'servico_entregador',
            'horario_funcionamento',
            'distancia',
            'latitude',
            'longitude',
            'telefone',
            'endereco',
        )

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
        cliente = (None, None)
        farmacia = (obj.latitude, obj.longitude)
        
        if 'pedido' in self.context:
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
        

class FarmaciaRetriveSerializer(FarmaciaPedidoSerializer):
    horarios = serializers.SerializerMethodField()

    class Meta:
        model = Farmacia
        fields = (
            'id',
            'cnpj',
            'valor_frete',
            'nome_fantasia',
            'tempo_entrega',
            'servico_entregador',
            'horario_funcionamento',
            'distancia',
            'latitude',
            'longitude',
            'telefone',
            'endereco',
            'horarios',
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
