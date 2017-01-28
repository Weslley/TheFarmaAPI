from thefarmaapi._celery import app
from api.management.commands.export_dados import update_dados_medicamentos as update_command


@app.task
def atualizacao():
    print('\nTeste\n')


@app.task
def update_dados_medicamentos(path, channel):
    update_command(path, channel)
