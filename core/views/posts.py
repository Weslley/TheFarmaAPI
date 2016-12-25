from awesome_mixins.mixins.list import ListMixin

from api.models.post import Post


class PostList(ListMixin):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 2
    search_default = ('titulo', '-data_atualizacao', 'Titulo')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    css_pagination = 'pagination pagination-success'
    columns = [
        {'lookup': 'titulo', 'name': 'Titulo'},
        {'lookup': 'tipo', 'name': 'Tipo', 'js_function': 'translate_tipo'},
        {'lookup': 'data_criacao', 'name': 'Data de criação', 'js_function': 'translate_datetime'},
        {'lookup': 'data_atualizacao', 'name': 'Atualização', 'js_function': 'translate_datetime'},
        {'lookup': 'usuario__first_name', 'name': 'Usuário'},
        {'lookup': 'usuario__user_instituicao__instituicao__nome_fantasia', 'name': 'Instituição', 'js_function': 'translate_instituicao'}
    ]

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        if not self.request.user.is_superuser:
            instituicao = self.request.user.user_instituicao.instituicao
            queryset = queryset.filter(
                usuario__user_instituicao__instituicao=instituicao
            )
        return queryset
