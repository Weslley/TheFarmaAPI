import re

from awesome_mixins.mixins.list import ListMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from api.models.farmacia import Farmacia
from api.models.representante_legal import RepresentanteLegal
from core.forms import FarmaciaForm, RepresentanteFarmaciaForm
from core.views.mixins import AdminBaseMixin


class FarmaciaList(ListMixin, AdminBaseMixin):
    model = Farmacia
    queryset = Farmacia.objects.all()
    paginate_by = 10
    search_default = ('razao_social', 'razao_social', 'Razão social')
    pagination_labels = {'prev': 'Anterior', 'next': 'Próximo', 'first': 'Primeiro', 'last': 'Último'}
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-body table-responsive'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    css_div_footer = 'box-footer'
    detail_url = '\'+ pk + \'/'
    columns = [
        {'lookup': 'razao_social', 'name': 'Razão social'},
        {'lookup': 'nome_fantasia', 'name': 'Nome fantasia'},
        {'lookup': 'telefone', 'name': 'Telefone'},
    ]


class FarmaciaCreate(CreateView, AdminBaseMixin):
    model = Farmacia
    form_class = FarmaciaForm
    success_url = reverse_lazy('farmacia-admin-list')

class FarmaciaDetail(DetailView, AdminBaseMixin):
    form_class = FarmaciaForm
    model = Farmacia
    pk_url_kwarg = 'id'
    template_name = 'api/farmacia_detail.html'

class RepresentanteCreate(CreateView, AdminBaseMixin):
    model = RepresentanteLegal
    form_class = RepresentanteFarmaciaForm

    def dispatch(self, request, *args, **kwargs):
        match = re.search('[0-9]+', request.META['PATH_INFO'])
        if match:
            farmacia_id = int(match.group())
            self.farmacia = Farmacia.objects.get(id=farmacia_id)
        return super(RepresentanteCreate, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def get_context_data(self, **kwargs):
        context = super(RepresentanteCreate, self).get_context_data(**kwargs)
        context['farmacia'] = self.farmacia
        return context

    def get_initial(self):
        return {'farmacia': self.farmacia}

    def get_success_url(self):
        self.success_url = reverse_lazy('farmacia-admin-view', kwargs={'id': self.object.farmacia.id})
        from django.utils.encoding import force_text
        self.success_url = force_text(self.success_url)
        url = self.success_url.format(**self.object.__dict__)
        return url

class RepresentanteDelete(DeleteView, AdminBaseMixin):
    model = RepresentanteLegal
    success_url = reverse_lazy('farmacia-admin-list')