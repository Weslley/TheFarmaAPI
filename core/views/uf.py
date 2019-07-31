from awesome_mixins.mixins.list import ListMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from api.models.atualizacao import Atualizacao
from api.models.uf import Uf
from core.views.mixins import AdminBaseMixin


class UfList(ListMixin, AdminBaseMixin):
    model = Uf
    queryset = Uf.objects.all()
    paginate_by = 27
    search_default = ('nome', 'nome', 'Nome')
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-content table-responsive'
    css_div_footer = 'box-footer'
    detail_url = '\'+ pk + \'/'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'sigla', 'name': 'Sigla'},
        {'lookup': 'nome', 'name': 'Nome'},
        {'lookup': 'icms', 'name': 'ICMS'},
    ]
    pagination_labels = {'prev': 'Anterior', 'next': 'Próximo', 'first': 'Primeiro', 'last': 'Último'}


class UfCreate(CreateView, AdminBaseMixin):
    model = Uf
    fields = ('nome', 'sigla', 'icms')
    success_url = reverse_lazy('uf-admin-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        Atualizacao.objects.create(usuario=self.request.user)
        instance.save()
        return super(UfCreate, self).form_valid(form)


class UfUpdate(UpdateView, AdminBaseMixin):
    model = Uf
    fields = ('nome', 'sigla', 'icms')
    success_url = reverse_lazy('uf-admin-list')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        instance = form.save(commit=False)
        Atualizacao.objects.create(usuario=self.request.user)
        instance.save()
        return super(UfUpdate, self).form_valid(form)
