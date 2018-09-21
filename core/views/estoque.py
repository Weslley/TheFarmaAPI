from awesome_mixins.mixins.list import ListMixin

from api.models.estoque import Estoque
from core.views.mixins import AdminBaseMixin


class EstoqueList(ListMixin, AdminBaseMixin):
    model = Estoque
    queryset = Estoque.objects.all()
    paginate_by = 10
    search_default = ('apresentacao__nome', '-apresentacao__nome', 'Apresentação')
    pagination_labels = {'prev': 'Anterior', 'next': 'Próximo', 'first': 'Primeiro', 'last': 'Último'}
    css_table = 'table'
    css_div_header = 'box-header'
    css_div_body = 'box-body table-responsive'
    # add_button_url = 'adicionar'
    # add_button_name = 'Adicionar'
    # O botao estava setado como false
    add_btn = False
    css_div_footer = ''
    detail_url = '\'+ pk + \'/'
    columns = [
        {'lookup': 'apresentacao__nome', 'name': 'Apresentação'},
        {'lookup': 'quantidade', 'name': 'Quantidade'},
        {'lookup': 'valor', 'name': 'Valor'},
        {'lookup': 'farmacia__razao_social', 'name': 'Farmacia'}
    ]
