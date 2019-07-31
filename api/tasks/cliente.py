from thefarmaapi._celery import app
from api.models.cliente import Cliente


@app.task(
    queue='update_cliente', autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'default_retry_delay': 60 * 3}
)
def update_foto_facebook(id_cliente, url):
    """
    Atualiza foto do cliente vinda do facebook
    :param id_cliente: Id do cliente
    :param url: URL da imagem
    :return:
    """
    cliente = Cliente.objects.get(id=id_cliente)
    cliente.get_remote_image(url)


