from django.db import transaction
from rest_framework import serializers

from api.models.farmacia import Farmacia
from api.models.feriado import Feriado
from api.serializers.conta_bancaria import ContaBancariaSerializer
from datetime import datetime

from api.serializers.endereco import EnderecoClienteCreateSerializer, EnderecoSerializer
from api.utils.generics import calcula_distancia
from api.utils.formats import formatar_telefone
from api.models.bairro import Bairro

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
            'valor_frete',
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
            'telefone',
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


class FarmaciaSimplificadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farmacia
        fields = (
            'cnpj', 'nome_fantasia', 'razao_social',
            'conta_bancaria', 'valor_frete', 'dia_pagamento',
            'percentual_similar', 'percentual_generico',
            'percentual_etico', 'percentual_nao_medicamentos'
        )


class FarmaciaRepresentanteSerializer(serializers.ModelSerializer):
    conta_bancaria = ContaBancariaSerializer()

    class Meta:
        model = Farmacia
        fields = (
            'cnpj', 'nome_fantasia', 'razao_social',
            'conta_bancaria', 'valor_frete'
        )

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


class FarmaciaComandaDado(serializers.ModelSerializer):

    logradouto = serializers.SerializerMethodField()
    bairro = serializers.SerializerMethodField()
    cidade = serializers.SerializerMethodField()
    telefone = serializers.SerializerMethodField()
    numero = serializers.SerializerMethodField()
    complemento = serializers.SerializerMethodField()

    class Meta:
        model = Farmacia
        fields = (
            'razao_social',
            'telefone',
            'logradouto',
            'bairro',
            'cidade',
            'numero',
            'complemento',
        )
    
    def get_logradouto(self,obj):
        try:
            return obj.endereco.logradouro
        except Exception as e:
            print(str(e))
            return ''
    
    def get_bairro(self,obj):
        # try:
        return obj.endereco.bairro

        # except Exception as e:
        #     print(str(e))
        #     return ''
        
    def get_cidade(self,obj):
        try:
            return '{} - {}'.format(obj.endereco.cidade.nome,obj.endereco.cidade.uf)
        except Exception as e:
            print(str(e))
            return ''

    def get_telefone(self,obj):
        return formatar_telefone(obj.telefone)
    
    def get_numero(self,obj):
        return obj.endereco.numero
    
    def get_complemento(self,obj):
        return obj.endereco.complemento