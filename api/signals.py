from pyrebase import pyrebase
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# from api.models.farmacia import Farmacia
# from api.models.laboratorio import Fabricante
# from api.models.medicamento import Produto
from api.models.post import Post
# from api.models.cidade import Cidade
from api.models.curtida import Curtida
# from api.models.principio_ativo import PrincipioAtivo
# from api.serializers.cidade import CidadeSerializer
# from api.serializers.farmacia import FarmaciaSerializer
# from api.serializers.laboratorio import LaboratorioSerializer
# from api.serializers.medicamento import MedicamentoSerializer
from api.serializers.post import PostExportSerializer

# from api.serializers.principio_ativo import PrincipioAtivoSerializer


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
