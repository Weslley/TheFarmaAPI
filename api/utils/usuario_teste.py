from api.management.commands.faker import Command as FakeCommand
import random
from api.models.pedido import ItemPropostaPedido

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
    #importa aqui pq treta 
    # esse modulo chama o modulo das serializer e o serializer chama ele
    from api.serializers.pedido import PropostaUpdateSerializer
    #data para salvar
    data = {
        'id':pedido.id
    }
    itens_proposta = []
    #recupera os itens pedidos
    itens = ItemPropostaPedido.objects.filter(pedido=pedido)
    for item in itens:
        #faz uma proposta aleatoria
        itens_proposta.append({
            'valor_unitario':random.randint(1,50),
            'quantidade':random.randint(1,item.quantidade),
            'possui':True,
            'id':item.id
        })
    #adiciona a lista de propostas
    data.update({
        'itens_proposta':itens_proposta    
    })
    #instancia o serializer e salva
    serializer = PropostaUpdateSerializer(pedido,data,partial=True)
    serializer.is_valid()
    serializer.save()


def criar_proposta_faramcia_teste(pedido):
    """
    Cria uma proposta da farmacia teste indepentende de onde esteja  
    """
    pass