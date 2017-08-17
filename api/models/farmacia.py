from datetime import time, timedelta

from django.db import models
from django.db.models import F, Sum

from api.models.configuracao import Configuracao
from api.models.conta_bancaria import ContaBancaria
from api.models.endereco import Endereco
from api.models.enums.status_item_proposta import StatusItemProposta
from api.utils.generics import calcula_distancia


class FarmaciaManager(models.Manager):

    def proximas(self, pedido, **kwargs):
        filter_queryset = {"representantes__usuario__auth_token__isnull": False}
        if pedido.cidade_obj:
            filter_queryset['endereco__cidade'] = pedido.cidade_obj

        queryset = self.filter(**filter_queryset)

        if 'exclude_farmacias' in kwargs and kwargs['exclude_farmacias']:
            queryset = queryset.exclude(id__in=[farmacia.id for farmacia in kwargs['exclude_farmacias']])

        try:
            raio_proposta = Configuracao.objects.first().raio_proposta
        except AttributeError:
            raio_proposta = 1.0
        except Exception as err:
            print(err)
            raio_proposta = 1.0

        result_list = [f for f in queryset if calcula_distancia(pedido.localizacao, f.localizacao) <= raio_proposta]

        return result_list


class Farmacia(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    razao_social = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    latitude = models.FloatField()
    longitude = models.FloatField()
    logo = models.ImageField(upload_to='farmacias', null=True, blank=True)
    endereco = models.OneToOneField(Endereco)
    data_criacao = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField(verbose_name='Data de atualização', auto_now_add=True)
    conta_bancaria = models.OneToOneField(ContaBancaria)
    servico_entregador = models.BooleanField(default=True)
    servico_estoque = models.BooleanField(default=False)
    percentual_similar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_generico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_etico = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentual_nao_medicamentos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tempo_entrega = models.DurationField(default=timedelta())
    horario_funcionamento_segunda_sexta_inicial = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_segunda_sexta_final = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_sabado_inicial = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_sabado_final = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_domindo_inicial = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_domindo_final = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_feriado_inicial = models.TimeField(default=time(0, 0, 0))
    horario_funcionamento_feriado_final = models.TimeField(default=time(0, 0, 0))
    objects = FarmaciaManager()

    class Meta:
        verbose_name = 'Farmácia'
        verbose_name_plural = 'Farmácias'

    def __str__(self):
        return self.razao_social

    @property
    def localizacao(self):
        """
        Localização do pedido
        :return: tupla de latitude e longitude
        """
        return self.latitude, self.longitude

    def get_itens_proposta(self, pedido):
        """
        Retorna itens da proposta
        :param pedido: Pedido proposto
        :return: retorna os itens numa queryset
        """
        return self.itens_proposta.filter(pedido=pedido)

    def get_status_proposta(self, pedido):
        """
        Retorna o status da proposta
        :param pedido: Pedido proposto
        :return: Status da proposta
        """
        # Verifica se todos os itens estão como enviado
        if all(item.status == StatusItemProposta.ENVIADO for item in self.get_itens_proposta(pedido)):
            return StatusItemProposta.ENVIADO

        # Verifica se todos os itens estão como cancelados
        if all(item.status == StatusItemProposta.CANCELADO for item in self.get_itens_proposta(pedido)):
            return StatusItemProposta.CANCELADO

        # caso contrario a proposta esta como em aberto
        return StatusItemProposta.ABERTO

    def get_valor_proposta(self, pedido):
        resultado = self.get_itens_proposta(pedido).aggregate(valor_proposta=Sum(
            F('quantidade') * F('valor_unitario'), output_field=models.DecimalField(max_digits=15, decimal_places=2)
        ))
        return resultado['valor_proposta']
