from django.core.management.base import BaseCommand
from api.models.apresentacao import Apresentacao
from misc.pusher_message import Message
import time



class Command(BaseCommand):
    help = 'Exportando os medicamentos identificados'

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
    with open(path,'w+') as f:
        #pega todos os identificados
        apresentacoes = Apresentacao.objects.filter(identificado=True).defer('id').values()
        #intera
        try:
            for item in apresentacoes:
                #linha da saida do arquivo
                linha = '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(item['codigo_barras'], item['dosagem'], item['sufixo_dosagem_id'], item['segunda_dosagem'], item['sufixo_segunda_dosagem_id'], item['terceira_dosagem'], item['sufixo_terceira_dosagem_id'], item['embalagem_id'], item['forma_farmaceutica_id'], item['quantidade'], item['sufixo_quantidade_id'], item['identificado'], item['pbm'], item['comercializado'], item['imagem'])
                #salva no arquivo
                f.write(linha)
                ok = ok + 1
                set_message(pusher_conn, 'update_message', '{} Produto exportado [OK]'.format(item['codigo_barras']))
        except Exception as e:
            error += 1
            print('Produto não exportado [FAIL]')
            print(str(e))
    #print balanço final
    print('Produtos {} OK\n Produtos {} FAIL'.format(ok,error))


def set_message(conn, method, message):
    if conn:
        conn.send(
            event=method,
            data={'mensagem': message}
        )