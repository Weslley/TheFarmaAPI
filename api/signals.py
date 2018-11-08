from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from pyrebase import pyrebase

from api.models.pedido import Pedido, LogData
from api.tasks.pedido import init_proposta

from api.models.curtida import Curtida
from api.models.post import Post
from api.serializers.post import PostExportSerializer


def update_model(model_name, data, remove=False):
    try:
        firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
        auth = firebase.auth()
        user = auth.current_user
        db = firebase.database()
        table = '{}s'.format(model_name)
        # row = {data['id']: data}
        if remove:
            db.child(table).child(str(data['id'])).remove()
        else:
            db.child(table).child(str(data['id'])).set(data)
    except Exception as err:
        print(err)


@receiver(post_save, sender=Pedido)
def create_log_de_datas(sender, instance, **kwargs):
    data = instance.data_criacao
    mes_pedido = data.strftime('%B')
    ano_pedido = data.year

    LogData.objects.get_or_create(
        mes=mes_pedido, ano=ano_pedido,
        farmacia=instance.farmacia
    )


@receiver(post_save, sender=Post)
def post_update_signal(sender, **kwargs):
    post = kwargs['instance']
    serializer = PostExportSerializer(post)
    data = serializer.data
    if post.ativo:
        update_model(sender.__name__.lower(), data)
    else:
        update_model(sender.__name__.lower(), data, True)


@receiver(post_delete, sender=Post)
def post_update_signal(sender, **kwargs):
    post = kwargs['instance']
    serializer = PostExportSerializer(post)
    data = serializer.data
    update_model(sender.__name__.lower(), data, True)


@receiver(post_save, sender=Curtida)
def curtida_crete_signal(sender, **kwargs):
    curtida = kwargs['instance']
    serializer = PostExportSerializer(curtida.post)
    data = serializer.data
    update_model('post', data)


@receiver(post_delete, sender=Curtida)
def curtida_delete_signal(sender, **kwargs):
    curtida = kwargs['instance']
    serializer = PostExportSerializer(curtida.post)
    data = serializer.data
    update_model('post', data)


@receiver(post_save, sender=Pedido)
def make_proposta(sender, **kwargs):
    if kwargs['created']:
        init_proposta.apply_async([kwargs['instance'].id, ], queue='propostas', countdown=1)
