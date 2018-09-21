from awesome_mixins.mixins.list import ListMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from api.models.atualizacao import Atualizacao
from api.models.produto import Produto
from core.views.mixins import AdminBaseMixin


class MedicamentoList(ListMixin, AdminBaseMixin):
    model = Produto
    queryset = Produto.objects.all()
    paginate_by = 10
    search_default = ('nome', '-data_atualizacao', 'Nome')
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-content table-responsive'
    css_div_footer = ''
    detail_url = '\'+ pk + \'/'
    # css_pagination = 'pagination pagination-success'
    pagination_labels = {'prev': 'Anterior', 'next': 'Próximo', 'first': 'Primeiro', 'last': 'Último'}
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'nome', 'name': 'Nome'},
        {'lookup': 'principio_ativo__nome', 'name': 'Principio Ativo'},
        {'lookup': 'laboratorio__nome', 'name': 'Laboratório'},
        {'lookup': 'tipo', 'name': 'Tipo', 'js_function': 'translate_tipo'},
        {'lookup': 'data_atualizacao', 'name': 'Atualização', 'js_function': 'translate_datetime'},
    ]


class MedicamentoCreate(CreateView, AdminBaseMixin):
    model = Produto
    fields = ('nome', 'principio_ativo', 'laboratorio', 'tipo')
    success_url = reverse_lazy('produto-admin-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        atualizacao = Atualizacao.objects.create(usuario=self.request.user)
        instance.data_atualizacao = atualizacao.data
        instance.save()
        return super(MedicamentoCreate, self).form_valid(form)


class MedicamentoUpdate(UpdateView, AdminBaseMixin):
    model = Produto
    fields = ('nome', 'principio_ativo', 'laboratorio', 'tipo')
    success_url = reverse_lazy('produto-admin-list')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        instance = form.save(commit=False)
        atualizacao = Atualizacao.objects.create(usuario=self.request.user)
        instance.data_atualizacao = atualizacao.data
        instance.save()
        return super(MedicamentoUpdate, self).form_valid(form)


class MedicamentoDetail(DetailView, AdminBaseMixin):
    model = Produto
    pk_url_kwarg = 'id'


class MedicamentoDelete(DeleteView, AdminBaseMixin):
    model = Produto
    success_url = reverse_lazy('produto-admin-list')
