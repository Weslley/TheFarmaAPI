from awesome_mixins.mixins.list import ListMixin

from api.models.post import Post


class PostList(ListMixin):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 10
    search_default = ('titulo', '-data_atualizacao', 'Titulo')
    css_class = {
        'table': 'table table-bordered table-condensed table-hover',
        'div_header': 'box-header',
        'div_body': 'box-body table-responsive no-padding',
        'div_footer': 'box-footer clearfix',
    }
    order_tags = [
        {'lookup': 'titulo', 'name': 'Titulo'},
        {'lookup': 'tipo', 'name': 'Tipo'},
        {'lookup': 'data_criacao', 'name': 'Data de criação'},
        {'lookup': 'data_atualizacao', 'name': 'Atualização'},
        {'lookup': 'usuario__first_name', 'name': 'Usuário'},
        {'lookup': 'usuario__user_instituicao__instituicao__nome_fantasia', 'name': 'Instituição'}
    ]
