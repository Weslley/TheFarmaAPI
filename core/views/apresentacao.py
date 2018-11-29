from awesome_mixins.mixins.list import ListMixin
from django.views.generic import UpdateView
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

# from api.models.atualizacao import Atualizacao
# from core.forms import AtualizacaoForm
# from core.tasks.task import update_dados_medicamentos

from api.models.apresentacao import Apresentacao
from core.views.mixins import AdminBaseMixin


class ApresentacaoList(ListMixin, AdminBaseMixin):
    model = Apresentacao
    queryset = Apresentacao.objects.all()
    paginate_by = 30
    search_default = ('codigo_barras', 'codigo_barras', 'Codigo de Barras')
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-body table-responsive'
    css_div_footer = 'box-footer'
    add_button_url = ''
    add_button_name = ''
    detail_url = '\'+ pk + \'/'
    columns = [
        {'lookup': 'codigo_barras', 'name': 'Código de Barras'},
        {'lookup': 'produto__nome', 'name': 'Produto'},
        {'lookup': 'identificado', 'name': 'Identificado', 'js_function': 'booleanfield'}
    ]


class ApresentacaoDetail(UpdateView, AdminBaseMixin):
    model = Apresentacao
    pk_url_kwarg = 'id'
    fields = (
        'dosagem', 'embalagem', 'sufixo_dosagem', 'identificado',
        'quantidade', 'sufixo_quantidade', 'imagem', 'forma_farmaceutica'
    )
    success_url = reverse_lazy('apresentacao-admin-list')
