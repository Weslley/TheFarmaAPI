import time
from datetime import date, datetime
from decimal import Decimal
import os
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models.apresentacao import Apresentacao
from api.models.fabricante import Fabricante
from api.models.principio_ativo import PrincipioAtivo
from api.models.produto import MedicamentoApExport, Produto
from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf
from api.utils.as3 import get_url_pre_signed,download_file
import urllib
from api.utils import tipo_produto
from misc.pusher_message import Message

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
        path = str(options['file'][0])
        update_dados_medicamentos(path)

def update_dados_medicamentos(path, channel='logs_command_line'):
    pusher_conn = Message('logs_command_line')
    laboratorios = {}
    principios_ativos = {}
    medicamentos_dict = {}
    medicamentos = []
    set_message(pusher_conn, 'update_message', '')
    time.sleep(1.5)
    set_message(pusher_conn, 'update_message', {'msg':'Inicializando dados do arquivo'})
    #recupera o arquivo
    path = download_file('media/' + path)
    print(path)
    try:
        with open(path, 'r', encoding="ISO-8859-1") as arq:
            with transaction.atomic():
                # Apagando todos os temporarios
                MedicamentoApExport.objects.all().delete()
                #le todas as linhas
                lines = arq.readlines()
                cont = 0
                #intera em cada linha
                for line in lines:
                    set_message(pusher_conn, 'update_message', {'msg':'Linha {}'.format(cont)})
                    #os dois primeiros digitos eh o tipo da linha(laboratiorio, medicamento, produto...)
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
                #recupera os medicamentos temporarios salvos, excluindo os sem codigo de barras
                medicamentos_temporarios = MedicamentoApExport.objects.exclude(codbarras='').values(
                    'laboratorio_id',
                    'descricao',
                    'principioAtivo_id'
                ).distinct()

                # Gerando os medicamentos(produtos)
                MAX_MED = medicamentos_temporarios.count()
                set_message(pusher_conn, 'update_message', 'Carregando e criando os medicamentos.')
                time.sleep(2)
                cont = 0
                #intera em todos os temporarios para criar uma lista de produtos
                for med_temp in medicamentos_temporarios:

                    med_temp = MedicamentoApExport.objects.filter(
                        laboratorio_id=med_temp['laboratorio_id'],
                        descricao=med_temp['descricao'],
                        principioAtivo_id=med_temp['principioAtivo_id']
                    ).first()
                    #verifica se tem e se nao tiver criar
                    medicamentos.append(get_or_create_medicamento(med_temp))
                    percent = int((50 / MAX_MED) * cont)
                    cont += 1
                    #set_message(pusher_conn, 'update_message', {'msg':'Carregando e criando os medicamentos.<br/>{}%'.format(percent)})

                # Gerando as apresenta????oes
                MAX_MED = len(medicamentos)
                set_message(pusher_conn, 'update_message', {'msg':'Atualizando apresenta????es.<br/>{}%'.format(percent)})
                cont = 0
                for med in medicamentos:
                    apresentacoes = MedicamentoApExport.objects.filter(
                        laboratorio_id=med.laboratorio_id,
                        descricao=med.nome,
                        principioAtivo_id=med.principio_ativo_id
                    ).exclude(codbarras='')

                    for ap in apresentacoes:
                        apresentacao = get_or_create_apresentacao(ap, med)
                        if apresentacao:
                            print('Atualizando medicamento {}'.format(med.id))
                            atualizando_tabelas(ap, apresentacao)

                    med_percent = (50 / MAX_MED) * cont
                    cont += 1
                    #set_message(pusher_conn, 'update_message', {'msg':'Atualizando apresenta????es.<br/>{}%'.format(int(percent + med_percent))})

                time.sleep(1)
                set_message(pusher_conn, 'update_message', 'Atualiza????o concluida.')
                time.sleep(2)
                set_message(pusher_conn, 'stop_load', '')
                print('Concluido com sucesso\n{} laboratorios\n{} principios ativos\n{} medicamentos\n{} apresentacoes\n{} tabelas de preco'.format(
                    len(laboratorios),
                    len(principios_ativos),
                    Produto.objects.count(),
                    Apresentacao.objects.count(),
                    TabelaPreco.objects.count()
                ))
    except Exception as err:
        print(err)
        time.sleep(1)
        set_message(pusher_conn, 'update_message', 'Erro ao realizar atualiza????o.')
        time.sleep(2)
        set_message(pusher_conn, 'stop_load', '')
    try:
        os.remove(path)
    except:
        print('nao apagou o arquivo')


def set_message(conn, method, message):
    if conn:
        conn.send(
            event=method,
            data={'mensagem': message}
        )


def exist_apresentacao(ap_temp):
    try:
        apresentacao = Apresentacao.objects.get(codigo_barras=ap_temp.codbarras)
        return True, apresentacao
    except Apresentacao.DoesNotExist:
        return False, None


def get_or_create_apresentacao(ap_temp, medicamento):
    try:
        exist, obj = exist_apresentacao(ap_temp)
        if exist:
            obj.nome = obj.nome.capitalize()
            obj.save()
            return obj

        if ap_temp.codbarras != '' and ap_temp.codbarras != '0':
            return Apresentacao.objects.create(
                codigo_barras=ap_temp.codbarras,
                nome=ap_temp.apresentacao.capitalize(),
                registro_ms=ap_temp.registroMS,
                produto=medicamento
            )
        else:
            return None
    except Apresentacao.MultipleObjectsReturned:
        return None


def exist_medicamento(med_temp):
    try:
        med = Produto.objects.get(
            principio_ativo_id=med_temp.principioAtivo_id,
            laboratorio_id=med_temp.laboratorio_id,
            nome=med_temp.descricao,
        )
        return True, med
    except:
        return False, None


def get_or_create_medicamento(med_temp):
    exist, obj = exist_medicamento(med_temp)
    if exist:
        obj.nome = obj.nome.capitalize()
        obj.save()
        return obj

    return Produto.objects.create(
        principio_ativo_id=med_temp.principioAtivo_id,
        laboratorio_id=med_temp.laboratorio_id,
        nome=med_temp.descricao,
        tipo=tipo_produto.GENERICO if med_temp.generico else tipo_produto.ETICO  # consultar com o gabriel
    )


def atualizando_tabelas(ap_temp, apresentacao):
    tabelas = []
    # tributa????es atuais
    for i in [12, 17, 18, 19]:
        tabela = get_or_create_tabela_preco(i, ap_temp, apresentacao)
        atualiza_preco(i, ap_temp, tabela)
        tabelas.append(tabela)
    return tabelas


def exist_tributacao(perc, apresentacao):
    try:
        tabela = TabelaPreco.objects.get(icms=perc, apresentacao=apresentacao)
        return True, tabela
    except TabelaPreco.DoesNotExist:
        return False, None


def atualiza_preco(perc, new_tab, old_tab):
    att = False

    # mudando o PMC
    if getattr(new_tab, 'pmc%d' % perc) != old_tab.pmc:
        old_tab.pmc = getattr(new_tab, 'pmc%d' % perc)
        old_tab.data_atualizacao = datetime.now()
        att = True
    # mudando o PMF
    if getattr(new_tab, 'pmf%d' % perc) != old_tab.pmf:
        old_tab.pmf = getattr(new_tab, 'pmf%d' % perc)
        old_tab.data_atualizacao = datetime.now()
        att = True

    if new_tab.dataVigencia != old_tab.data_vigencia:
        old_tab.data_vigencia = new_tab.dataVigencia
        old_tab.data_atualizacao = datetime.now()
        att = True

    if att:
        print('Att algum')
        old_tab.save()


def get_or_create_tabela_preco(perc, ap_temp, apresentacao):
    exist, obj = exist_tributacao(perc, apresentacao)
    if exist:
        return obj
    return TabelaPreco.objects.create(
        icms=perc,
        pmc=getattr(ap_temp, 'pmc%d' % perc),
        pmf=getattr(ap_temp, 'pmf%d' % perc),
        data_vigencia=ap_temp.dataVigencia,
        apresentacao=apresentacao,
    )


def add_laboratorio(line):
    """
    Cria laboratorio
    :param line:
    :return:
    """
    try:
        lab = Fabricante.objects.get(id=int(line[2:5]))
        lab.nome = line[5:25].strip()
        lab.razao_social = line[25:65].strip()
        lab.save()
        return lab
    except Fabricante.DoesNotExist:
        return Fabricante.objects.create(
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
        tmp = MedicamentoApExport.objects.get(id=int(line[2:8] if len(line[2:8].strip()) else 0))
        tmp.descricao = tpm.descricao.capitalize()
        tmp.apresentacao = tpm.apresentacao.capitalize()
        tmp.save()
        return tmp
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
            descricao=line[71:106].strip().capitalize(),
            apresentacao=line[106:151].strip().capitalize(),
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