from api.models.pedido import ItemPropostaPedido
from django.db.models import Avg

def get_preco_medio(id, quant=100):
    """
    Retorna o preco medio de uma apresentacao analisando X precos propostos
    id Int
    return Int
    """
    try:
        precos = ItemPropostaPedido.objects.values('id','valor_unitario')\
                                            .filter(apresentacao_id=id)[:quant]\
                                            .aggregate(Avg('valor_unitario'))
        return precos['valor_unitario__avg']
    except Exception as e:
        print(str(e))
        return 0

