from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from api.models.instituicao import Instituicao
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy


class InstituicaoList(ListMixin, AdminBaseMixin):
    model = Instituicao
    queryset = Instituicao.objects.all()
    paginate_by = 10
    search_default = ('nome_fantasia', 'nome_fantasia', 'Nome fantasia')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
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
