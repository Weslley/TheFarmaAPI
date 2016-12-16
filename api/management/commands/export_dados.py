from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
from decimal import Decimal

from api.models.apresentacao import Apresentacao
from api.models.laboratorio import Laboratorio
from api.models.medicamento import MedicamentoApExport, Medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf
from api.utils import tipo_medicamento

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
        medicamentos_dict = {}
        medicamentos = []
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
                        med = add_medicamento_temp(line)
                        medicamentos_dict[med.id] = med

                medicamentos_temporarios = MedicamentoApExport.objects.values(
                    'laboratorio_id',
                    'descricao',
                    'principioAtivo_id'
                ).distinct()

                # Apagando dados anteriores
                TabelaPreco.objects.all().delete()
                Apresentacao.objects.all().delete()
                Medicamento.objects.all().delete()

                # Gerando os medicamentos
                for med_temp in medicamentos_temporarios:
                    med_temp = MedicamentoApExport.objects.filter(
                        laboratorio_id=med_temp['laboratorio_id'],
                        descricao=med_temp['descricao'],
                        principioAtivo_id=med_temp['principioAtivo_id']
                    ).first()
                    medicamentos.append(Medicamento.objects.create(
                        principio_ativo_id=med_temp.principioAtivo_id,
                        laboratorio_id=med_temp.laboratorio_id,
                        nome=med_temp.descricao,
                        tipo=tipo_medicamento.GENERICO if med_temp.generico else tipo_medicamento.ETICO # consultar com o gabriel
                    ))

                # Gerando as apresentaçãoes
                for med in medicamentos:
                    apresentacoes = MedicamentoApExport.objects.filter(
                        laboratorio_id=med.laboratorio_id,
                        descricao=med.nome,
                        principioAtivo_id=med.principio_ativo_id
                    )
                    for ap in apresentacoes:
                        apresentacao = Apresentacao.objects.create(
                            codigo_barras=0,  # Perguntar para o gabriel qual codigo de barras colocar
                            nome=ap.apresentacao,
                            registro_ms=ap.registroMS,
                            medicamento=med
                        )
                        # gerando as tabelas de precos
                        tabelas = [
                            # Tabela 12
                            TabelaPreco.objects.create(
                                icms=12,
                                pmc=ap.pmc12,
                                pmf=ap.pmf12,
                                data_vigencia=ap.dataVigencia,
                                apresentacao=apresentacao,
                            ),
                            # Tabela 17
                            TabelaPreco.objects.create(
                                icms=17,
                                pmc=ap.pmc17,
                                pmf=ap.pmf17,
                                data_vigencia=ap.dataVigencia,
                                apresentacao=apresentacao,
                            ),
                            # Tabela 18
                            TabelaPreco.objects.create(
                                icms=18,
                                pmc=ap.pmc18,
                                pmf=ap.pmf18,
                                data_vigencia=ap.dataVigencia,
                                apresentacao=apresentacao,
                            ),
                            # Tabela 19
                            TabelaPreco.objects.create(
                                icms=19,
                                pmc=ap.pmc19,
                                pmf=ap.pmf19,
                                data_vigencia=ap.dataVigencia,
                                apresentacao=apresentacao,
                            )
                        ]

                        for tabela in tabelas:
                            siglas = []
                            if tabela.icms == 0:
                                pass
                            elif tabela.icms == 12:
                                pass
                            elif tabela.icms == 17:
                                siglas = ['AC', 'AL', 'CE', 'DF', 'ES', 'GO', 'MT', 'MS', 'PA', 'PI', 'RR', 'SC']
                            elif tabela.icms == 17.5:
                                siglas = ['RO', ]
                            elif tabela.icms == 18:
                                siglas = ['AM', 'AP', 'BA', 'MA', 'MG', 'PB', 'PE', 'PR', 'RN', 'RS', 'SE', 'SP', 'TO']
                            elif tabela.icms == 20:
                                siglas = ['RJ', ]

                            ufs = Uf.objects.filter(sigla__in=siglas)
                            for uf in ufs:
                                tabela.ufs.add(uf)

                print('Concluido com sucesso\n{} laboratorios\n{} principios ativos\n{} medicamentos\n{} apresentações\n{} tabelas de preço'.format(
                    len(laboratorios),
                    len(principios_ativos),
                    Medicamento.objects.count(),
                    Apresentacao.objects.count(),
                    TabelaPreco.objects.count()
                ))


def add_laboratorio(line):
    """
    Cria laboratorio
    :param line:
    :return:
    """
    try:
        lab = Laboratorio.objects.get(id=int(line[2:5]))
        lab.nome = line[5:25].strip()
        lab.razao_social = line[25:65].strip()
        lab.save()
        return lab
    except Laboratorio.DoesNotExist:
        return Laboratorio.objects.create(
            id=int(line[2:5]),
            nome=line[5:25].strip(),
            razao_social=line[25:65].strip()
        )


def add_principio_ativo(line):
    """
    Cria Principi ativo
    :param line:
    :return:
    """
    try:
        principio = PrincipioAtivo.objects.get(id=int(line[2:7]))
        principio.nome = line[7:27].strip()
        principio.save()
        return principio
    except PrincipioAtivo.DoesNotExist:
        return PrincipioAtivo.objects.create(
            id=int(line[2:7]),
            nome=line[7:27].strip()
        )


def add_medicamento_temp(line):
    """
    Gera o medicamento temporario
    :param line:
    :return:
    """
    try:
        return MedicamentoApExport.objects.get(id=int(line[2:8] if len(line[2:8].strip()) else 0))
    except MedicamentoApExport.DoesNotExist:
        return MedicamentoApExport.objects.create(
            id=int(line[2:8]),
            familia=int(line[8:12]),
            principioAtivo_id=int(line[12:17]),
            classe=int(line[17:21]),
            subClasse=int(line[21:25]),
            laboratorio_id=int(line[25:28]),
            codbarras=line[28:41].strip(),
            codbarras2=line[41:54].strip(),
            codbarras3=line[54:67].strip(),
            tipoPreco=line[67:68].strip(),
            lista=line[68:69].strip(),
            vazio=line[69:70].strip(),
            generico=False if line[70:71] == 'N' else True,
            descricao=line[71:106].strip().upper(),
            apresentacao=line[106:151].strip().upper(),
            dataVigencia=date(day=int(line[151:159].strip()[0:2]), month=int(line[151:159].strip()[2:4]), year=int(line[151:159].strip()[4:8])) if len(line[151:159].strip()) == 8 else None,
            dataDesconhecida=date(day=int(line[159:167].strip()[0:2]), month=int(line[159:167].strip()[2:4]), year=int(line[159:167].strip()[4:8])) if len(line[159:167].strip()) == 8 else None,
            pmf19=Decimal(line[167:175]) / 100 if Decimal(line[167:175]) != Decimal(0) else Decimal(0),
            pmf18=Decimal(line[175:183]) / 100 if Decimal(line[175:183]) != Decimal(0) else Decimal(0),
            pmf17=Decimal(line[183:191]) / 100 if Decimal(line[183:191]) != Decimal(0) else Decimal(0),
            pmf12=Decimal(line[191:199]) / 100 if Decimal(line[191:199]) != Decimal(0) else Decimal(0),
            pmc19=Decimal(line[199:207]) / 100 if Decimal(line[199:207]) != Decimal(0) else Decimal(0),
            pmc18=Decimal(line[207:215]) / 100 if Decimal(line[207:215]) != Decimal(0) else Decimal(0),
            pmc17=Decimal(line[215:223]) / 100 if Decimal(line[215:223]) != Decimal(0) else Decimal(0),
            pmc12=Decimal(line[223:231]) / 100 if Decimal(line[223:231]) != Decimal(0) else Decimal(0),
            registroMS=line[231:246].strip(),
            portaria=line[246:256].strip(),
        )
