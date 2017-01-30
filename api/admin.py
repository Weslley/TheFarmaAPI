# -*- coding: utf-8 -*-

from django.contrib import admin

from api.models.atualizacao import Atualizacao
from api.models.curtida import Curtida
from api.models.perfil import Perfil
from api.models.post import Post
from api.models.representante_legal import RepresentanteLegal
from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf
from api.models.apresentacao import Apresentacao
from api.models.bairro import Bairro
from api.models.cidade import Cidade
from api.models.endereco import Endereco
from api.models.farmacia import Farmacia
from api.models.laboratorio import Laboratorio
from api.models.medicamento import Medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.instituicao import Instituicao, UsuarioInstituicao


# class FarmaciaAdmin(admin.ModelAdmin):
#     list_display = (
#         'cnpj',
#         'razao_social',
#         'nome_responsavel',
#         'cliente_infog2',
#         'telefone',
#         'bairro'
#     )
#     list_display_links = list_display
#     list_filter = ('cliente_infog2', 'cidade', 'bairro')
#     list_per_page = 10
#     fieldsets = (
#         (
#             'Dados da Farmácia',
#             {
#                 'fields': (
#                     ('cnpj', 'cliente_infog2'),
#                     ('razao_social', 'nome_fantasia'),
#                     ('telefone', 'latitude', 'longitude'),
#                 )
#             }
#         ),
#         (
#             'Endereço da Farmácia',
#             {
#                 'fields': (
#                     ('cep', 'logradouro', 'numero'),
#                     'complemento',
#                     ('cidade',  'bairro'),
#                 )
#             }
#         ),
#         (
#             'Dados do Responsável',
#             {
#                 'fields': (
#                     ('nome_responsavel', 'sobrenome_responsavel'),
#                     'telefone_responsavel',
#                     ('rg_responsavel', 'cpf_responsavel'),
#                 )
#             }
#         ),
#         (
#             'Endereço do Responsável',
#             {
#                 'fields': (
#                     ('cep_responsavel', 'logradouro_responsavel', 'numero_responsavel'),
#                     'complemento_responsavel',
#                     ('cidade_responsavel',  'bairro_responsavel'),
#                 )
#             }
#         ),
#     )
#     search_fields = (
#         'cnpj',
#         'razao_social',
#         'nome_responsavel',
#         'telefone',
#         'bairro',
#         'nome_fantasia',
#         'cidade',
#         'logradouro'
#     )
#     ordering = ('id',)

from api.utils.reverse_admin import ReverseModelAdmin


class FarmaciaAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    list_display = ('get_cidade', )
    fieldsets = (
        (
            'Dados da Farmácia',
            {
                'fields': (
                    ('cnpj', 'nome_fantasia', 'razao_social'),
                    ('telefone', 'cliente_infog2', 'logo'),
                    ('usuario', ),
                )
            }
        ),
    )

    inline_reverse = (
        'endereco',
    )

    def get_cidade(self, obj):
        return obj.endereco.cidade

    get_cidade.short_description = 'Cidade'
    get_cidade.admin_order_field = 'endereco__cidade'


class PerfilAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    list_display = ('get_nome', )
    fieldsets = (
        (
            'Dados da Farmácia',
            {
                'fields': (
                    ('sexo', 'sobre'),
                )
            }
        ),
    )

    declared_fieldsets = (
        (
            'Dados Principais',
            {
                'fields': (
                    ('first_name', 'last_name')
                )
            }
        ),
    )

    inline_reverse = (
        'usuario',
    )


    def get_nome(self, obj):
        return obj.usuario.first_name

    get_nome.short_description = 'Nome'
    get_nome.admin_order_field = 'usuario__nome'


class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'likes', 'data_criacao', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': (
                'titulo',
                'conteudo',
                'tipo',
                ('imagem', 'video'),
                'url_referencia'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(Farmacia, FarmaciaAdmin)
admin.site.register(Medicamento)
admin.site.register(PrincipioAtivo)
admin.site.register(Laboratorio)
admin.site.register(Endereco)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Uf)
admin.site.register(RepresentanteLegal)
admin.site.register(Apresentacao)
admin.site.register(TabelaPreco)
admin.site.register(Post, PostAdmin)
admin.site.register(Perfil)
admin.site.register(Curtida)
admin.site.register(Atualizacao)
admin.site.register(Instituicao)
admin.site.register(UsuarioInstituicao)
