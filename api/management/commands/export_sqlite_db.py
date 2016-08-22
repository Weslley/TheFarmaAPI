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
        cursor.execute("""SELECT * FROM medicine;""")
        medicamentos_table = cursor.fetchall()
        max_med = 15357
        cont = 0
        principios_salvos = {}
        laboratorios_salvos = {}
        grupos_salvos = {}
        print('Iniciando exportação...')
        with transaction.atomic():
            for linha in medicamentos_table:
                cont += 1
                # criando dicionario representando o medicamento
                med_row = dict(zip(colunas, linha))

                try:
                    Medicamento.objects.get(codigo_barras=med_row['barr_code'])
                except Medicamento.DoesNotExist:
                    # criando o medicamento e memória
                    medicamento = Medicamento(
                        codigo_barras=med_row['barr_code'],
                        registro=med_row['register_number'],
                        nome=med_row['name'].strip(),
                        nome_complementar=med_row['name_complement'].strip(),
                        generico=True if med_row['generic'] == 1 else False,
                        tipo=med_row['type'],
                        preco_maximo=med_row['max_price']
                    )

                    # Buscando o pricipio ativo
                    id_principio = principios_salvos[med_row['active_ingredient_id']] if med_row['active_ingredient_id'] in principios_salvos else None
                    if not id_principio:
                        cursor.execute(
                            """SELECT name FROM active_ingredient WHERE id = ?;""",
                            (med_row['active_ingredient_id'],)
                        )
                        r = cursor.fetchone()
                        principio = PrincipioAtivo.objects.create(nome=r[0])
                        medicamento.principio_ativo = principio
                        principios_salvos[med_row['active_ingredient_id']] = principio.id
                    else:
                        principio = PrincipioAtivo.objects.get(id=id_principio)
                        medicamento.principio_ativo = principio

                    # buscando laboratorios
                    id_laboratorio = laboratorios_salvos[med_row['laboratory_id']] if med_row['laboratory_id'] in laboratorios_salvos else None
                    if not id_laboratorio:
                        cursor.execute(
                            """SELECT name, full_name FROM laboratory WHERE id = ?;""",
                            (med_row['laboratory_id'],)
                        )
                        r = cursor.fetchone()
                        laboratorio = Laboratorio.objects.create(nome=r[0], nome_completo=r[1])
                        medicamento.laboratorio = laboratorio
                        laboratorios_salvos[med_row['laboratory_id']] = laboratorio.id
                    else:
                        laboratorio = Laboratorio.objects.get(id=id_laboratorio)
                        medicamento.laboratorio = laboratorio

                    # buscando o grupo
                    id_grupo = grupos_salvos[med_row['group_id']] if med_row['group_id'] in grupos_salvos else None
                    if not id_grupo:
                        cursor.execute(
                            """SELECT name, item_count FROM medicine_group WHERE id = ?;""",
                            (med_row['group_id'],)
                        )
                        r = cursor.fetchone()
                        grupo = GrupoMedicamento.objects.create(nome=r[0], quantidade=r[1], principio_ativo=principio)
                        medicamento.grupo = grupo
                        grupos_salvos[med_row['group_id']] = grupo.id
                    else:
                        grupo = GrupoMedicamento.objects.get(id=id_grupo)
                        medicamento.grupo = grupo

                    # salvando o medicamento
                    medicamento.save()



                perc = (cont*100) / max_med
                print('Exportação dos medicamentos em andamento: %.2f%%\r' % perc)

            # Buscando o pricipio ativo
            print('Verificando principios')
            cursor.execute(
                """SELECT name, id FROM active_ingredient WHERE id NOT IN %s;""" % str(tuple(id for id in principios_salvos.keys()))
            )
            principio_table = cursor.fetchall()
            for linha in principio_table:
                principio = PrincipioAtivo.objects.create(nome=linha[0])
                principios_salvos[linha[1]] = principio.id

            # Buscando laboratórios
            print('Verificando laboratórios')
            cursor.execute("""SELECT name, full_name FROM laboratory WHERE id NOT IN %s;""" % str(tuple(id for id in laboratorios_salvos.keys()))
            )
            lab_table = cursor.fetchall()
            for linha in lab_table:
                Laboratorio.objects.create(nome=linha[0], nome_completo=linha[1])

            # Buscando grupos
            print('Verificando Grupos')
            cursor.execute("""SELECT name, item_count, active_ingredient_id FROM medicine_group WHERE id NOT IN %s;""" % str(tuple(id for id in grupos_salvos.keys()))
            )
            group_table = cursor.fetchall()
            for linha in group_table:
                if linha[2]:
                    princ_id = principios_salvos[linha[2]]
                    GrupoMedicamento.objects.create(nome=linha[0], quantidade=linha[1], principio_ativo_id=princ_id)
                else:
                    GrupoMedicamento.objects.create(nome=linha[0], quantidade=linha[1])

            print('Exportação concluida com sucesso.')


