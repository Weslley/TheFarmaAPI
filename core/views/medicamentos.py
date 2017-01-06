from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from api.models.medicamento import Medicamento
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from api.models.atualizacao import Atualizacao


class MedicamentoList(ListMixin, AdminBaseMixin):
    model = Medicamento
    queryset = Medicamento.objects.all()
    paginate_by = 10
    search_default = ('nome', '-data_atualizacao', 'Nome')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    detail_url = '\'+ id + \'/'
    # css_pagination = 'pagination pagination-success'
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
    model = Medicamento
    fields = ('nome', 'principio_ativo', 'laboratorio', 'tipo')
    success_url = reverse_lazy('medicamento-admin-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        atualizacao = Atualizacao.objects.create()
        instance.data_atualizacao = atualizacao.data
        instance.save()
        return super(MedicamentoCreate, self).form_valid(form)


class MedicamentoUpdate(UpdateView, AdminBaseMixin):
    model = Medicamento
    fields = ('nome', 'principio_ativo', 'laboratorio', 'tipo')
    success_url = reverse_lazy('medicamento-admin-list')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        instance = form.save(commit=False)
        atualizacao = Atualizacao.objects.create()
        instance.data_atualizacao = atualizacao.data
        instance.save()
        return super(MedicamentoUpdate, self).form_valid(form)


class MedicamentoDetail(DetailView, AdminBaseMixin):
    model = Medicamento
    pk_url_kwarg = 'id'


class MedicamentoDelete(DeleteView, AdminBaseMixin):
    model = Medicamento
    success_url = reverse_lazy('medicamento-admin-list')
