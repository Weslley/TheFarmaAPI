from django.core.management.base import BaseCommand
from django.db import transaction

from api.models.laboratorio import Laboratorio

TIPO_LABORATORIO = 1
TIPO_NAO_USADO2 = 2
TIPO_NAO_USADO3 = 3
TIPO_NAO_USADO4 = 4
TIPO_PRINCIPIO_ATIVO = 5
TIPO_MEDICAMENTO = 6
TIPO_SUBSTANCIA_BASICA = 7


class Command(BaseCommand):
    help = 'Exportando com base no arquivo'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        laboratorios = {}
        principios_ativos = {}
        with open(str(options['file'][0]), 'rb') as arq:
            with transaction.atomic():
                lines = arq.readlines()
                cont = 0
                for line in lines:
                    tipo = int(line[:2])
                    cont += 1
                    if tipo == TIPO_LABORATORIO:
                        lab = add_laboratorio(line)
                        laboratorios[cont] = lab
                    elif tipo == TIPO_PRINCIPIO_ATIVO:
                        principio = add_principio_ativo(line)
                        principios_ativos[cont] = principio

                print('Concluido, {} laboratorios e {} principios ativos'.format(len(laboratorios), len(principios_ativos)))


def add_laboratorio(line):
    return Laboratorio.objects.create(
        id=line[2:5],

    )


def add_principio_ativo(line):
    return line
