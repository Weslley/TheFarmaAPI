from api.management.commands.export_dados import \
    update_dados_medicamentos as update_command
from thefarmaapi._celery import app


@app.task
def atualizacao():
    print('\nTeste\n')


@app.task(queue='default')
def update_dados_medicamentos(path, channel):
    update_command(path, channel)
