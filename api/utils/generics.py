import re


class Converter:
    """
    Classe com metodos de conversão
    """

    @classmethod
    def snake_case(cls, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_client_ip(request):
    """
    Retorna o IP da requisição
    :param request: Request
    :return: Ip da mesma
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    """
    Retorna o Agent(Browser) da requisição
    :param request: Request
    :return: Agent
    """
    agent = request.META.get('HTTP_USER_AGENT')
    return agent


def get_user_lookup(request, lookup):
    """
    Retorna o objeto passado como lookup
    :param request: Request
    :param lookup: String do nome do lookup
    :return: Objeto relacionado ao user
    """
    if hasattr(request.user, lookup):
        return getattr(request.user, lookup, None)
    return None
