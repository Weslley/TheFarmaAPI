from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from api.models.farmacia import Farmacia
from django.views.generic import CreateView
from api.models.representante_legal import RepresentanteLegal
from core.forms import RepresentanteFarmaciaForm, FarmaciaForm
from django.urls import reverse_lazy


class FarmaciaList(ListMixin, AdminBaseMixin):
    model = Farmacia
    queryset = Farmacia.objects.all()
    paginate_by = 10
    search_default = ('razao_social', 'razao_social', 'Razão social')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    css_div_footer = ''
    columns = [
        {'lookup': 'razao_social', 'name': 'Razão social'},
        {'lookup': 'nome_fantasia', 'name': 'Nome fantasia'},
        {'lookup': 'telefone', 'name': 'Telefone'},
        {'lookup': 'cliente_infog2', 'name': 'Cliente INFOG2'},
    ]


class FarmaciaCreate(CreateView, AdminBaseMixin):
    model = Farmacia
    form_class = FarmaciaForm
    success_url = reverse_lazy('farmacia-admin-list')


class RepresentanteCreate(CreateView, AdminBaseMixin):
    model = RepresentanteLegal
    form_class = RepresentanteFarmaciaForm
    success_url = reverse_lazy('post-admin-list')
