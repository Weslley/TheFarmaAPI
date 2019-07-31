from django.core.management.base import BaseCommand
from api.models.apresentacao import Apresentacao
from misc.pusher_message import Message
import time



class Command(BaseCommand):
    help = 'Atualiza as apresentacoes dos produtos'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        path = str(options['file'][0])
        exportar(path)


def exportar(path, channel=None):
    #init vars
    pusher_conn = Message(channel) if channel else None
    ok = 0
    error = 0
    #inicial pusher
    set_message(pusher_conn, 'update_message', '')
    time.sleep(1.5)
    set_message(pusher_conn, 'update_message', 'Inicializando dados do arquivo')
    with open(path,'r') as f:
        #intera em todas as linhas
        for line in f.readlines():
            aux = line.split(' ')
            #recupera a apresentacao
            try:
                apresentacao = Apresentacao.objects.get(codigo_barras=aux[0])
            except Exception as e:
                print('Falha em recuperar {}'.format(aux[0]))
                set_message(pusher_conn, 'update_message', 'Falha em recuperar {}'.format(aux[0]))
                error += 1
            try:
                #atualiza
                if aux[1] != 'None':
                    apresentacao.dosagem = aux[1]
                if aux[2] != 'None':
                    apresentacao.sufixo_dosagem_id = aux[2]
                if aux[3] != 'None':
                    apresentacao.segunda_dosagem = aux[3]
                if aux[4] != 'None':
                    apresentacao.sufixo_segunda_dosagem_id = aux[4]
                if aux[5] != 'None':
                    apresentacao.terceira_dosagem = aux[5]
                if aux[6] != 'None':
                    apresentacao.sufixo_terceira_dosagem_id = aux[6]
                if aux[7] != 'None':
                    apresentacao.embalagem_id = aux[7]
                if aux[8] != 'None':
                    apresentacao.forma_farmaceutica_id = aux[8]
                if aux[9] != 'None':
                    apresentacao.quantidade = aux[9]
                if aux[10] != 'None':
                    apresentacao.sufixo_quantidade_id = aux[10]
                if aux[11] != 'None':
                    apresentacao.identificado = aux[11]
                if aux[12] != 'None':
                    apresentacao.pbm = aux[12]
                if aux[13] != 'None':
                    apresentacao.comercializado = aux[13]
                if aux[14] != 'None':
                    apresentacao.imagem = aux[14]
                apresentacao.save()
                ok += 1
                print('OK')
                set_message(pusher_conn, 'update_message', '{} Produto atualizado [OK]'.format(aux[0]))
            except Exception as e:
                print('Falha em salvar {}'.format(aux[0]))
                print(str(e))
                set_message(pusher_conn, 'update_message', 'Falha em salvar {}'.format(aux[0]))

def set_message(conn, method, message):
    if conn:
        conn.send(
            event=method,
            data={'mensagem': message}
        )