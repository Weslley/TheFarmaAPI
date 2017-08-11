from awesome_mixins.mixins.list import ListMixin

from api.models.estoque import Estoque
from core.views.mixins import AdminBaseMixin


class EstoqueList(ListMixin, AdminBaseMixin):
    model = Estoque
    queryset = Estoque.objects.all()
    paginate_by = 10
    search_default = ('apresentacao__nome', '-apresentacao__nome', 'Apresentação')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    add_btn = False
    css_div_footer = ''
    columns = [
        {'lookup': 'apresentacao__nome', 'name': 'Apresentação'},
        {'lookup': 'quantidade', 'name': 'Quantidade'},
        {'lookup': 'valor', 'name': 'Valor'},
        {'lookup': 'farmacia__razao_social', 'name': 'Farmacia'}
    ]
