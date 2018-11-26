from django.contrib import admin

from api.models.administradora import Administradora, Parcelamento
from api.models.apresentacao import Apresentacao, \
    ImagemApresentacao, Unidade, FormaFarmaceutica, Sufixo, Embalagem
from api.models.atualizacao import Atualizacao
from api.models.bairro import Bairro
from api.models.banco import Banco
from api.models.cartao import Cartao
from api.models.cidade import Cidade
from api.models.cliente import Cliente, ClienteEndereco
from api.models.configuracao import Configuracao
from api.models.conta_bancaria import ContaBancaria
from api.models.conta_pagar import ContaPagar
from api.models.conta_receber import ContaReceber
from api.models.curtida import Curtida
from api.models.endereco import Endereco
from api.models.estoque import Estoque
from api.models.fabricante import Fabricante
from api.models.farmacia import Farmacia
from api.models.feriado import Feriado
from api.models.log import Log
from api.models.parceiro import Parceiro, UsuarioParceiro
from api.models.pedido import ItemPedido, ItemPropostaPedido, Pedido, LogData
from api.models.post import Post
from api.models.principio_ativo import PrincipioAtivo
from api.models.produto import Produto
from api.models.representante_legal import RepresentanteLegal
from api.models.secao import Secao
from api.models.sintoma import Sintoma
from api.models.subsecao import Subsecao
from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf
from api.models.regiao import Regiao
from api.models.conta import Conta
from api.models.boleto import Boleto

from api.utils.reverse_admin import ReverseModelAdmin

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
                ('tipo', 'ativo'),
                ('imagem', 'video'),
                'url_referencia'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'status', 'data_vencimento', 'valor_liquido')


class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'status', 'data_vencimento', 'valor_parcela')


class ImagemInline(admin.StackedInline):
    model = ImagemApresentacao
    extra = 1

class ApresentacaoAdmin(admin.ModelAdmin):
    inlines = [ImagemInline]
    readonly_fields = ('codigo_barras', 'registro_ms', 'produto', 'nome')
    fields = (
        'produto', 'codigo_barras', 'registro_ms', 'nome',
        'identificado', 'comercializado', 'pbm',
        'forma_farmaceutica', 'embalagem',
        'dosagem', 'sufixo_dosagem',
        'quantidade', 'sufixo_quantidade',
    )
    list_filter = ('forma_farmaceutica', 'comercializado', 'identificado', 'pbm')
    list_display = (
        'nome', 'get_nome_da_apresentacao', 'produto',
        'codigo_barras', 'get_possui_imagem', 'identificado'
    )
    search_fields = ('codigo_barras', 'registro_ms', 'produto__nome')

    def get_nome_da_apresentacao(self, obj):
        if obj.forma_farmaceutica:
            if obj.sufixo_quantidade:
                return "{0}{1}, {2} com {3}{4}".format(
                    obj.dosagem, obj.sufixo_dosagem,
                    obj.forma_farmaceutica.nome, obj.quantidade,
                    obj.sufixo_quantidade
                )
            return "{0}{1}, {2} {3}".format(
                obj.dosagem, obj.sufixo_dosagem,
                obj.quantidade, obj.forma_farmaceutica.nome.lower()
            )
        return "{}".format(obj)

    get_nome_da_apresentacao.short_description = 'Nome Formatado'

    def get_possui_imagem(self, obj):
        if obj.imagens:
            if obj.imagens.exists():
                return "Sim"
        return "Não"

    get_possui_imagem.short_description = 'Possui Imagem'

admin.site.register(Embalagem)
admin.site.register(Sufixo)
admin.site.register(FormaFarmaceutica)
admin.site.register(Boleto)
admin.site.register(Conta)
admin.site.register(Farmacia)
admin.site.register(Produto)
admin.site.register(PrincipioAtivo)
admin.site.register(LogData)
admin.site.register(Fabricante)
admin.site.register(Endereco)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Uf)
admin.site.register(RepresentanteLegal)
admin.site.register(Apresentacao, ApresentacaoAdmin)
admin.site.register(TabelaPreco)
admin.site.register(Post, PostAdmin)
admin.site.register(Cliente)
admin.site.register(Curtida)
admin.site.register(Atualizacao)
admin.site.register(Parceiro)
admin.site.register(UsuarioParceiro)
admin.site.register(ImagemApresentacao)
admin.site.register(Unidade)
admin.site.register(Secao)
admin.site.register(Subsecao)
admin.site.register(ClienteEndereco)
admin.site.register(Estoque)
admin.site.register(Sintoma)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Cartao)
admin.site.register(Banco)
admin.site.register(ContaBancaria)
admin.site.register(Log)
admin.site.register(ContaPagar, ContaPagarAdmin)
admin.site.register(ContaReceber, ContaReceberAdmin)
admin.site.register(ItemPropostaPedido)
admin.site.register(Configuracao)
admin.site.register(Feriado)
admin.site.register(Administradora)
admin.site.register(Parcelamento)
admin.site.register(Regiao)