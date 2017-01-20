from thefarmaapi.celery import app


@app.task
def atualizacao():
    print('\nTeste\n')
