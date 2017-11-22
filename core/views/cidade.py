import re

from awesome_mixins.mixins.list import ListMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView

from api.models.cidade import Cidade
from api.models.representante_legal import RepresentanteLegal
from core.views.mixins import AdminBaseMixin


class CidadeList(ListMixin, AdminBaseMixin):
    model = Cidade
    queryset = Cidade.objects.all()
    paginate_by = 10
    search_default = ('nome', 'nome', 'Nome')
    pagination_labels = {'prev': 'Anterior', 'next': 'Próximo', 'first': 'Primeiro', 'last': 'Último'}
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-body table-responsive'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    css_div_footer = 'box-footer'
    detail_url = '\'+ pk + \'/'
    columns = [
        {'lookup': 'ibge', 'name': 'Código IBGE', 'width': 150},
        {'lookup': 'nome', 'name': 'Nome'},
        {'lookup': 'uf__sigla', 'name': 'UF'},
    ]


class CidadeCreate(CreateView, AdminBaseMixin):
    model = Cidade
    fields = ('ibge', 'nome', 'uf')
    success_url = reverse_lazy('cidade-admin-list')


class CidadeDetail(DetailView, AdminBaseMixin):
    model = Cidade
    pk_url_kwarg = 'id'
