from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_exempt
from api.models.bairro import Bairro


@ajax
@csrf_exempt
def busca_bairro_cidade(request):
    id_cidade = request.GET['id_cidade']
    if not id_cidade:
        return {'items': None}

    q = request.GET['q']
    return {'items': [{'id': b.id, 'text': b.nome} for b in Bairro.objects.filter(nome__icontains=q, cidade_id=id_cidade)]}
