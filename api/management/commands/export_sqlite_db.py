# -*- coding: utf-8 -*-
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import *


class Command(BaseCommand):
    help = 'Comando para exporta dados dos medicamento do Banco SQLITE3'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sqlite_path', nargs='+', type=str)

    def handle(self, *args, **options):
        # conectando ao banco
        conn = sqlite3.connect(options['sqlite_path'][0])
        cursor = conn.cursor()

        # lendo colunas dos medicamentos
        cursor.execute('PRAGMA table_info({})'.format('medicine'))
        colunas = [tupla[1] for tupla in cursor.fetchall()]
        cursor.execute("""SELECT * FROM dados;""")
        medicamentos_table = cursor.fetchall()
        for row in medicamentos_table:
            print(row)
            input('Tecle Enter')


