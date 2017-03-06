from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from api.models.instituicao import Instituicao, UsuarioInstituicao
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from core.forms import UsuarioInstituicaoForm
import re


class InstituicaoList(ListMixin, AdminBaseMixin):
    model = Instituicao
    queryset = Instituicao.objects.all()
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


class InstituicaoCreate(CreateView, AdminBaseMixin):
    model = Instituicao
    fields = (
        'razao_social',
        'nome_fantasia',
        'cpf_cnpj',
        'site',
        'logo',
        'telefone'
    )

    success_url = reverse_lazy('instituicao-admin-list')


class InstituicaoUpdate(UpdateView, AdminBaseMixin):
    model = Instituicao
    fields = (
        'razao_social',
        'nome_fantasia',
        'cpf_cnpj',
        'site',
        'logo',
        'telefone'
    )
    success_url = reverse_lazy('instituicao-admin-list')


class InstituicaoDetail(DetailView, AdminBaseMixin):
    model = Instituicao
    pk_url_kwarg = 'id'


class UsuarioInstituicaoCreate(CreateView, AdminBaseMixin):
    model = UsuarioInstituicao
    form_class = UsuarioInstituicaoForm

    def dispatch(self, request, *args, **kwargs):
        match = re.search('[0-9]+', request.META['PATH_INFO'])
        if match:
            farmacia_id = int(match.group())
            self.instituicao = Instituicao.objects.get(id=farmacia_id)
        return super(UsuarioInstituicaoCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioInstituicaoCreate, self).get_context_data(**kwargs)
        context['instituicao'] = self.instituicao
        return context

    def get_initial(self):
        return {'instituicao': self.instituicao}

    def get_success_url(self):
        self.success_url = reverse_lazy('instituicao-admin-view', kwargs={'id': self.object.instituicao.id})
        from django.utils.encoding import force_text
        self.success_url = force_text(self.success_url)
        url = self.success_url.format(**self.object.__dict__)
        return url
