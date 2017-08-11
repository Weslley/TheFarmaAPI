import re

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from awesome_mixins.mixins.list import ListMixin

from core.forms import UsuarioParceiroForm
from core.views.mixins import AdminBaseMixin
from api.models.parceiro import Parceiro, UsuarioParceiro


class ParceiroList(ListMixin, AdminBaseMixin):
    model = Parceiro
    queryset = Parceiro.objects.all()
    paginate_by = 10
    search_default = ('nome_fantasia', 'nome_fantasia', 'Nome fantasia')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    detail_url = '\'+ id + \'/'
    # css_pagination = 'pagination pagination-success'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'razao_social', 'name': 'Razão social'},
        {'lookup': 'nome_fantasia', 'name': 'Nome fantasia'},
        {'lookup': 'cpf_cnpj', 'name': 'CPF/CNPJ'},
        {'lookup': 'telefone', 'name': 'Telefone'},
        {'lookup': 'data_criacao', 'name': 'Data criação'},
    ]


class ParceiroCreate(CreateView, AdminBaseMixin):
    model = Parceiro
    fields = (
        'razao_social',
        'nome_fantasia',
        'cpf_cnpj',
        'site',
        'logo',
        'telefone'
    )

    success_url = reverse_lazy('parceiro-admin-list')


class ParceiroUpdate(UpdateView, AdminBaseMixin):
    model = Parceiro
    fields = (
        'razao_social',
        'nome_fantasia',
        'cpf_cnpj',
        'site',
        'logo',
        'telefone'
    )
    success_url = reverse_lazy('parceiro-admin-list')


class ParceiroDetail(DetailView, AdminBaseMixin):
    model = Parceiro
    pk_url_kwarg = 'id'


class UsuarioParceiroCreate(CreateView, AdminBaseMixin):
    model = UsuarioParceiro
    form_class = UsuarioParceiroForm

    def dispatch(self, request, *args, **kwargs):
        match = re.search('[0-9]+', request.META['PATH_INFO'])
        if match:
            farmacia_id = int(match.group())
            self.parceiro = Parceiro.objects.get(id=farmacia_id)
        return super(UsuarioParceiroCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioParceiroCreate, self).get_context_data(**kwargs)
        context['parceiro'] = self.parceiro
        return context

    def get_initial(self):
        return {'parceiro': self.parceiro}

    def get_success_url(self):
        self.success_url = reverse_lazy('parceiro-admin-view', kwargs={'id': self.object.parceiro.id})
        from django.utils.encoding import force_text
        self.success_url = force_text(self.success_url)
        url = self.success_url.format(**self.object.__dict__)
        return url
