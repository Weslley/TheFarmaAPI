from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from awesome_mixins.mixins.list import ListMixin

from api.utils import tipo_post
from api.models.post import Post
from core.views.mixins import AdminBaseMixin


class PostList(ListMixin, AdminBaseMixin):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 10
    search_default = ('titulo', '-data_atualizacao', 'Titulo')
    css_table = 'table'
    css_div_header = 'card-header'
    css_div_body = 'card-content table-responsive'
    css_div_footer = ''
    detail_url = '\'+ id + \'/'
    add_button_url = 'adicionar'
    add_button_name = 'Adicionar'
    columns = [
        {'lookup': 'titulo', 'name': 'Titulo'},
        {'lookup': 'tipo', 'name': 'Tipo', 'js_function': 'translate_tipo'},
        {'lookup': 'data_criacao', 'name': 'Data de criação', 'js_function': 'translate_datetime'},
        {'lookup': 'data_atualizacao', 'name': 'Atualização', 'js_function': 'translate_datetime'},
        {'lookup': 'usuario__first_name', 'name': 'Usuário'},
        {'lookup': 'usuario__user_instituicao__instituicao__nome_fantasia', 'name': 'Instituição', 'js_function': 'translate_instituicao'},
        {'lookup': 'ativo', 'name': 'Ativo', 'js_function': 'translate_ativo'}
    ]

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        if not self.request.user.is_superuser:
            instituicao = self.request.user.user_instituicao.instituicao
            queryset = queryset.filter(
                usuario__user_instituicao__instituicao=instituicao
            )
        return queryset


class PostCreate(CreateView, AdminBaseMixin):
    model = Post
    fields = ('titulo', 'conteudo', 'tipo', 'imagem', 'video', 'url_referencia', 'ativo')
    success_url = reverse_lazy('post-admin-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        if not self.request.user.is_superuser:
            instance.tipo = tipo_post.PATROCINADO
        instance.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView, AdminBaseMixin):
    model = Post
    pk_url_kwarg = 'id'
    fields = ('titulo', 'conteudo', 'imagem', 'video', 'url_referencia', 'ativo', 'tipo')
    success_url = reverse_lazy('post-admin-list')


class PostDetail(DetailView, AdminBaseMixin):
    model = Post
    pk_url_kwarg = 'id'


class PostDelete(DeleteView, AdminBaseMixin):
    model = Post
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('post-admin-list')
