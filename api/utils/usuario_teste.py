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
    c = FakeCommand()
    c.logar('x@x.com','teste@1234') #loga
    c.monta_headers() #monta os headers
    c.fazer_proposta({'id':pedido.id}) #faz a proposta
