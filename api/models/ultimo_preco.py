from api.models.farmacia import Farmacia
from api.models.apresentacao import Apresentacao
from decimal import Decimal
from django.db import models

class UltimoPreco(models.Model):
    apresentacao = models.ForeignKey(Apresentacao,on_delete=models.DO_NOTHING,related_name='ultimo_pedido_apresentacao',null=False,blank=False)
    farmacia = models.ForeignKey(Farmacia,on_delete=models.DO_NOTHING,related_name='ultimo_pedido_farmacia',null=False,blank=False)
    valor = models.DecimalField(max_digits=15,decimal_places=2,default=Decimal(0),null=True,blank=True)
    