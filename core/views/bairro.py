import re

from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django_ajax.decorators import ajax

from api.models.bairro import Bairro
from api.models.cidade import Cidade
from core.views.mixins import AdminBaseMixin


@ajax
@csrf_exempt
def busca_bairro_cidade(request):
    id_cidade = request.GET['id_cidade']
    if not id_cidade:
        return {'items': None}

    q = request.GET['q']
    return {'items': [{'id': b.id, 'text': b.nome} for b in Bairro.objects.filter(nome__icontains=q, cidade_id=id_cidade)]}


class BairroCreate(CreateView, AdminBaseMixin):
    model = Bairro
    fields = ('nome', 'cidade')

    def dispatch(self, request, *args, **kwargs):
        match = re.search('[0-9]+', request.META['PATH_INFO'])
        if match:
            bairro_id = int(match.group())
            self.cidade = Cidade.objects.get(ibge=bairro_id)
        return super(BairroCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BairroCreate, self).get_context_data(**kwargs)
        context['cidade'] = self.cidade
        return context

    def get_initial(self):
        return {'cidade': self.cidade}

    def get_success_url(self):
        self.success_url = reverse_lazy('cidade-admin-view', kwargs={'id': self.object.cidade.ibge})
        from django.utils.encoding import force_text
        self.success_url = force_text(self.success_url)
        url = self.success_url.format(**self.object.__dict__)
        return url
