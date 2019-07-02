from django.db import models
from django.contrib.postgres.fields import JSONField
from .enums.tipo_notificacao import TipoNotificacao
from api.models.pedido import Pedido


class TipoNotificacaoTemplate():
    VISUALIZADO = 1
    NOVA_PROPOSTA = 2
    SEM_RESPOSTA = 8
    MEDICAMENTO_AGUARDANDO_RETIRADA_S = 4
    MEDICAMENTO_AGUARDANDO_RETIRADA_P = 5
    MEDICAMENTO_SAIU_ENTREGA_S = 6
    MEDICAMENTO_SAIU_ENTREGA_P = 3
    MEDICAMENTO_FORAM_ENTREGUE_S = 9
    MEDICAMENTO_FORAM_ENTREGUE_P = 7
    FARMACIA_CANCELOU = 10
    PEDIDO_SEM_ESTOQUE = 11
    ENDERECO_NAO_LOCALIZADO = 12
    DINHEIRO_ESTORNADO = 13
    #PEDIDO_ACEITO = 14
    #B_ >> BUSCA; D_ >> DELIVERY
    B_AGUARDANDO_EM_DINHEIRO_NORM = 15
    B_AGUARDANDO_EM_DINHEIRO_COM_RECEITA = 16
    B_AGUARDANDO_EM_CARTAO_NORM = 17
    B_AGUARDANDO_EM_CARTAO_COM_RECEITA = 18
    D_AGUARDANDO_EM_CARTAO_NORM = 19
    D_AGUARDANDO_EM_CARTAO_COM_RECEITA = 20
    D_AGUARDANDO_EM_DINHEIRO_NORM = 21
    D_AGUARDANDO_EM_DINHEIRO_COM_RECEITA = 22
    D_PEDIDO_ENTREGUE = 23


class Notificacao(models.Model):
    tipo = models.IntegerField(choices=TipoNotificacao.choices())
    titulo = models.CharField(max_length=50)
    mensagem = models.TextField(null=True, blank=True)
    mensagem_extra = models.TextField(null=True, blank=True)
    visualizada = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=True, blank=True)
    cliente = models.ForeignKey(
        'Cliente',
        related_name='notificacoes',
        on_delete=models.CASCADE
    )
    pedido = models.ForeignKey(Pedido,models.CASCADE,default=None,null=True,blank=True)

    def __str__(self):
        return self.titulo

class NotificacoesTemplate(models.Model):
    tela = models.IntegerField(null=True,blank=True)
    titulo = models.CharField(max_length=50,null=True,blank=True)
    menssagem = models.TextField(null=True, blank=True)
    mensagem_extra = models.TextField(null=True, blank=True)
    tipo = models.IntegerField(null=True,blank=True)