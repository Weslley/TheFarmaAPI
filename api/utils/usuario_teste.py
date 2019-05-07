from api.management.commands.faker import Command as FakeCommand
import random
from decimal import Decimal
from api.models.pedido import ItemPropostaPedido
from api.models.enums.status_item_proposta import StatusItemProposta

def check_user_eh_teste(user):
    """
    Verifica se eh o usuario teste  
    user: User  
    return: Bool  
    """
    if user.id == 119:
        return True
    else:
        return False

def fazer_proposta_faker(pedido):
    """
    Farmacia teste faz uma propostas falsa  
    pedido: Pedido  
    """
    #recupera os itens pedidos
    itens = ItemPropostaPedido.objects.filter(pedido=pedido)
    for item in itens:
        #faz uma proposta aleatoria
        item.valor_unitario = Decimal(random.randint(1,50))
        item.quantidade = random.randint(1,item.quantidade)
        item.status = 1
        item.possui = True
        item.save()
    print('proposta fake feita')

def criar_proposta_faramcia_teste(pedido):
    """
    Cria uma proposta da farmacia teste indepentende de onde esteja  
    """
    pass