# -*- coding: utf-8 -*-
import sqlite3
from datetime import date

from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import *
from api.models.apresentacao import Apresentacao
from api.models.laboratorio import Laboratorio
from api.models.medicamento import Medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf


class Command(BaseCommand):
    help = 'Comando para exporta dados dos medicamento do Banco SQLITE3'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sqlite_path', nargs='+', type=str)

    def handle(self, *args, **options):
        # conectando ao banco
        DATABASE_URL = options['sqlite_path'][0]
        # export_principios(DATABASE_URL)
        # export_laboratorios()

        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        # lendo colunas dos medicamentos
        medicamentos_table = search_medicamentos(cursor)
        cont = 0
        for cnpj, med, principio in medicamentos_table:
            try:
                with transaction.atomic():
                    # Buscando laboratorio
                    laboratorio = Laboratorio.objects.get(cnpj=clean_cnpj(cnpj))
                    # Buscando principio ativo
                    principio_ativo = PrincipioAtivo.objects.get(nome=clean_principio(principio))
                    # Salvando medicamento
                    medicamento = create_medicamento(**{
                        'nome': med.strip(), 'principio_ativo': principio_ativo, 'laboratorio': laboratorio, 'tipo': 2
                    })
                    # Carregando as apresentações
                    apresentacoes = search_apresentacoes(cursor, *[cnpj, med, principio])

                    # Iterando para salvar as apresentações
                    for nome, ean, registro_ms, pf_0, pmc_0, pf_12, pmc_12, pf_17, pmc_17, pf_17_5, pmc_17_5, pf_18, pmc_18, pf_20, pmc_20, ultima_alteracao in apresentacoes:
                        cont += 1
                        # Salvando apresentação
                        apresentacao = create_apresentacao(**{
                            'codigo_barras': int(ean.strip()),
                            'nome': nome.strip(),
                            'registro_ms': registro_ms.strip(),
                            'medicamento': medicamento
                        })
                        # # Salvando as tabelas de preço
                        create_tabelas(
                            apresentacao,
                            [
                                (0, pf_0.strip(), pmc_0.strip()),
                                (12, pf_12.strip(), pmc_12.strip()),
                                (17, pf_17.strip(), pmc_17.strip()),
                                (17.5, pf_17_5.strip(), pmc_17_5.strip()),
                                (18, pf_18.strip(), pmc_18.strip()),
                                (20, pf_20.strip(), pmc_20.strip())
                            ],
                            ultima_alteracao
                        )
                        print('{} - Apresentação: {} salva com sucesso.'.format(cont, nome))
            except Exception as err:
                print(err)
                print(type(err))
                input('')


def export_principios(database_url):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("""SELECT principio_ativo FROM dados GROUP BY principio_ativo;""")
    principios = cursor.fetchall()
    for p in principios:
        p = p[0]
        p = p.strip()
        p = p.replace(';', ', ')
        PrincipioAtivo.objects.create(nome=p)
        print('Principio salvo - {}'.format(p))


def export_laboratorios():
    arq = open('laboratorios.csv')
    linhas = arq.readlines()
    try:
        for linha in linhas:
            cnpj, nome = linha.split(';')
            cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
            nome = nome.strip()
            Laboratorio.objects.create(
                cnpj=cnpj,
                nome=nome
            )
            print('Laoratório salvo com sucesso- CNPJ: {}, NOME: {}'.format(cnpj, nome))
    except Exception as err:
        print(err)


def create_apresentacao(**kwargs):
    return Apresentacao.objects.create(**kwargs)


def create_medicamento(**kwargs):
    return Medicamento.objects.create(**kwargs)


def create_tabelas(apresentacao, precos, vigencia):
    try:
        dia, mes, ano = vigencia.strip().split('/')
        vigencia = date(ano, mes, dia)
    except:
        vigencia = None

    for icms, pmf, pmc in precos:
        if pmf or pmc:
            if pmf.replace(',', '').replace('.', '').isdigit():
                pmf = pmf.replace(',', '.')
                pmf = Decimal(pmf)
            else:
                pmf = Decimal(0)

            if pmc:
                pmc = pmc.replace(',', '.')
                pmc = Decimal(pmc)
            else:
                pmc = Decimal(0)

            tabela = create_tabela(**{
                'icms': Decimal(icms), 'pmf': pmf, 'pmc': pmc, 'data_vigencia': vigencia, 'apresentacao': apresentacao
            })

            siglas = []
            if icms == 0:
                pass
            elif icms == 12:
                pass
            elif icms == 17:
                siglas = ['AC', 'AL', 'CE', 'DF', 'ES', 'GO', 'MT', 'MS', 'PA', 'PI', 'RR', 'SC']
                pass
            elif icms == 17.5:
                siglas = ['RO', ]
                pass
            elif icms == 18:
                siglas = ['AM', 'AP', 'BA', 'MA', 'MG', 'PB', 'PE', 'PR', 'RN', 'RS', 'SE', 'SP', 'TO' ]
                pass
            elif icms == 20:
                siglas = ['RJ', ]
                pass

            if siglas:
                ufs = Uf.objects.filter(sigla__in=siglas)
                for uf in ufs:
                    tabela.ufs.add(uf)


def create_tabela(**kwargs):
    return TabelaPreco.objects.create(**kwargs)


def search_medicamentos(cursor):
    cursor.execute("""
        SELECT cnpj, medicamento, principio_ativo FROM dados GROUP BY cnpj, medicamento, principio_ativo;
    """)
    return cursor.fetchall()


def search_apresentacoes(cursor, *args):
    cursor.execute("""
        SELECT apresentacao, ean, registro_ms, pf_0, pmc_0, pf_12, pmc_12, pf_17, pmc_17, pf_17_5, pmc_17_5, pf_18, pmc_18, pf_20, pmc_20, ultima_alteracao
        FROM dados
        WHERE cnpj = '{}' AND medicamento = '{}' AND principio_ativo = '{}';
    """.format(*args))
    return cursor.fetchall()


def clean_cnpj(cnpj):
    cnpj = cnpj.strip()
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    return cnpj


def clean_principio(principio):
    principio = principio.strip()
    principio = principio.replace(';', ', ')
    principio = principio.strip()
    return principio
