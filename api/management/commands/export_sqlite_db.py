# -*- coding: utf-8 -*-
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import *
from api.models.laboratorio import Laboratorio
from api.models.principio_ativo import PrincipioAtivo


class Command(BaseCommand):
    help = 'Comando para exporta dados dos medicamento do Banco SQLITE3'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sqlite_path', nargs='+', type=str)

    def handle(self, *args, **options):
        # conectando ao banco
        DATABASE_URL = options['sqlite_path'][0]
        # self.export_principios(DATABASE_URL)
        # self.export_laboratorios()

        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        # lendo colunas dos medicamentos
        cursor.execute('PRAGMA table_info({})'.format('medicine'))
        colunas = [tupla[1] for tupla in cursor.fetchall()]
        cursor.execute("""
            SELECT cnpj, medicamento, principio_ativo FROM dados GROUP BY cnpj, medicamento, principio_ativo;
        """)
        cont = 0
        medicamentos_table = cursor.fetchall()
        for cnpj, medicamento, principio in medicamentos_table:
            laboratorio = Laboratorio.objects.get(cnpj=clean_cnpj(cnpj))
            principio_ativo = PrincipioAtivo.objects.get(nome=clean_principio(principio))
            # print(laboratorio)
            # print(principio_ativo)
            print('{}'.format(medicamento))
            cursor.execute("""
            SELECT apresentacao, ean, pmc_0, pmc_12, pmc_17, pmc_17_5, pmc_18, pmc_20, ultima_alteracao
            FROM dados
            WHERE cnpj = '{}' AND medicamento = '{}' AND principio_ativo = '{}';
            """.format(
                cnpj, medicamento, principio
            ))
            apresentacoes = cursor.fetchall()
            for apresentacao, ean, pmc_0, pmc_12, pmc_17, pmc_17_5, pmc_18, pmc_20, ultima_alteracao in apresentacoes:
                cont += 1
                print("""
                Apresentação: {}\n
                Codigo de barras: {}\n
                PMC 0%: {}\n
                PMC 12%: {}\n
                PMC 17%: {}\n
                PMC 17,5%: {}\n
                PMC 18%: {}\n
                PMC 20%: {}\n
                Ultima alteração%: {}
                """.format(apresentacao, ean, pmc_0, pmc_12, pmc_17, pmc_17_5, pmc_18, pmc_20, ultima_alteracao))
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==')
        print(cont)


    def export_principios(self, database_url):
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



    def export_laboratorios(self):
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


def clean_cnpj(cnpj):
    cnpj = cnpj.strip()
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    return cnpj


def clean_principio(principio):
    principio = principio.strip()
    principio = principio.replace(';', ', ')
    principio = principio.strip()
    return principio
