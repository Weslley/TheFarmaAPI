# -*- coding: utf-8 -*-

from django.contrib import admin
from api.models import *


class FarmaciaAdmin(admin.ModelAdmin):
    list_display = (
        'cnpj',
        'razao_social',
        'nome_responsavel',
        'cliente_infog2',
        'telefone',
        'bairro'
    )
    list_display_links = list_display
    list_filter = ('cliente_infog2', 'cidade', 'bairro')
    list_per_page = 10
    fieldsets = (
        (
            'Dados da Farmácia',
            {
                'fields': (
                    ('cnpj', 'cliente_infog2'),
                    ('razao_social', 'nome_fantasia'),
                    ('telefone', 'latitude', 'longitude'),
                )
            }
        ),
        (
            'Endereço da Farmácia',
            {
                'fields': (
                    ('cep', 'logradouro', 'numero'),
                    'complemento',
                    ('cidade',  'bairro'),
                )
            }
        ),
        (
            'Dados do Responsável',
            {
                'fields': (
                    ('nome_responsavel', 'sobrenome_responsavel'),
                    'telefone_responsavel',
                    ('rg_responsavel', 'cpf_responsavel'),
                )
            }
        ),
        (
            'Endereço do Responsável',
            {
                'fields': (
                    ('cep_responsavel', 'logradouro_responsavel', 'numero_responsavel'),
                    'complemento_responsavel',
                    ('cidade_responsavel',  'bairro_responsavel'),
                )
            }
        ),
    )
    search_fields = (
        'cnpj',
        'razao_social',
        'nome_responsavel',
        'telefone',
        'bairro',
        'nome_fantasia',
        'cidade',
        'logradouro'
    )
    ordering = ('id',)


admin.site.register(Farmacia, FarmaciaAdmin)
admin.site.register(Cidade)
admin.site.register(Medicamento)
admin.site.register(GrupoMedicamento)
admin.site.register(PrincipioAtivo)
admin.site.register(Laboratorio)
