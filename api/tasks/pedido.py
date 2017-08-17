from thefarmaapi._celery import app


@app.task(queue='propostas')
def init_proposta(pedido=None):
    print(pedido)
    print('INICIANDO PROPOSTA')
