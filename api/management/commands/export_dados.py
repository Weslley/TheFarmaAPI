from django.core.management.base import BaseCommand
from django.db import transaction

from api.management.commands.medicamento_export import ApresentacaoExport
from api.models.laboratorio import Laboratorio
from api.models.principio_ativo import PrincipioAtivo

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
        with open(str(options['file'][0]), 'r', encoding="ISO-8859-1") as arq:
            with transaction.atomic():
                lines = arq.readlines()
                cont = 0
                for line in lines:
                    tipo = int(line[:2])
                    cont += 1
                    if tipo == TIPO_LABORATORIO:
                        lab = add_laboratorio(line)
                        laboratorios[lab.id] = lab
                    elif tipo == TIPO_PRINCIPIO_ATIVO:
                        principio = add_principio_ativo(line)
                        principios_ativos[principio.id] = principio
                    elif tipo == TIPO_MEDICAMENTO:
                        print(line[17:21])

                print('Concluido, {} laboratorios e {} principios ativos'.format(len(laboratorios), len(principios_ativos)))


def add_laboratorio(line):
    try:
        lab = Laboratorio.objects.get(id=int(line[2:5]))
        lab.nome = line[5:25]
        lab.razao_social = line[25:65]
        lab.save()
        return lab
    except Laboratorio.DoesNotExist:
        return Laboratorio.objects.create(
            id=int(line[2:5]),
            nome=line[5:25],
            razao_social=line[25:65]
        )


def add_principio_ativo(line):
    try:
        principio = PrincipioAtivo.objects.get(id=int(line[2:7]))
        principio.nome = line[7:27]
        principio.save()
        return principio
    except PrincipioAtivo.DoesNotExist:
        return PrincipioAtivo.objects.create(
            id=int(line[2:7]),
            nome=line[7:27]
        )


def add_medicamento(line, laboratorios, principios):
    return ApresentacaoExport(line, laboratorios, principios)
