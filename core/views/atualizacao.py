from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from api.models.atualizacao import Atualizacao
from django.views.generic import CreateView
from django.urls import reverse_lazy
from core.forms import AtualizacaoForm
from core.tasks.task import update_dados_medicamentos


class AtualizacaoList(ListMixin, AdminBaseMixin):
    model = Atualizacao
    queryset = Atualizacao.objects.all()
    paginate_by = 10
    search_default = ('data', '-data', 'Data da atualização')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'data', 'name': 'Data da atualização', 'js_function': 'translate_datetime', 'width': 200},
        {'lookup': 'usuario__first_name', 'name': 'Usuário'},
    ]


class AtualizacaoCreate(CreateView, AdminBaseMixin):
    model = Atualizacao
    form_class = AtualizacaoForm
    success_url = reverse_lazy('atualizacao-admin-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        instance.save()
        update_dados_medicamentos.apply_async([instance.arquivo.path, self.request.session.session_key])
        return super(AtualizacaoCreate, self).form_valid(form)
