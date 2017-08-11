from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from awesome_mixins.mixins.list import ListMixin

from api.models.uf import Uf
from core.views.mixins import AdminBaseMixin
from api.models.atualizacao import Atualizacao


class UfList(ListMixin, AdminBaseMixin):
    model = Uf
    queryset = Uf.objects.all()
    paginate_by = 27
    search_default = ('nome', 'nome', 'Nome')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    detail_url = '\'+ id + \'/'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'sigla', 'name': 'Sigla'},
        {'lookup': 'nome', 'name': 'Nome'},
        {'lookup': 'icms', 'name': 'ICMS'},
    ]


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
