from api.management.commands.faker import Command as FakeCommand

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
    c = FakeCommand()
    print('ola')
    c.logar('x@x.com','teste@1234') #loga
    c.monta_headers() #monta os headers
    c.fazer_proposta({'id':pedido.id}) #faz a proposta


def criar_proposta_faramcia_teste(pedido):
    """
    Cria uma proposta da farmacia teste indepentende de onde esteja  
    """
    pass