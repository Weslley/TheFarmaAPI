from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pyrebase import pyrebase
from django.conf import settings

from api.models.cidade import Cidade
from api.models.curtida import Curtida
from api.models.farmacia import Farmacia
from api.models.laboratorio import Laboratorio
from api.models.medicamento import Medicamento
from api.models.post import Post
from api.models.principio_ativo import PrincipioAtivo
from api.serializers.cidade import CidadeSerializer
from api.serializers.farmacia import FarmaciaSerializer
from api.serializers.laboratorio import LaboratorioSerializer
from api.serializers.medicamento import MedicamentoSerializer
from api.serializers.post import PostExportSerializer
from api.serializers.principio_ativo import PrincipioAtivoSerializer


def update_model(model_name, data):
    try:
        firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
        auth = firebase.auth()
        user = auth.current_user
        db = firebase.database()
        table = '{}s'.format(model_name)
        # row = {data['id']: data}
        db.child(table).child(str(data['id'])).set(data)
    except Exception as err:
        print(err)

#
# @receiver(post_save, sender=Medicamento)
# def teste_signal(sender, **kwargs):
#     serializer = MedicamentoSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)
#
#
# @receiver(post_save, sender=Medicamento)
# def medicamento_update_signal(sender, **kwargs):
#     serializer = MedicamentoSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)
#
#
# @receiver(post_save, sender=Farmacia)
# def farmacia_update_signal(sender, **kwargs):
#     serializer = FarmaciaSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)
#
#
# @receiver(post_save, sender=Cidade)
# def cidade_update_signal(sender, **kwargs):
#     serializer = CidadeSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)
#
#
# @receiver(post_save, sender=PrincipioAtivo)
# def principio_ativo_update_signal(sender, **kwargs):
#     serializer = PrincipioAtivoSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)
#
#
# @receiver(post_save, sender=Laboratorio)
# def laboratorio_update_signal(sender, **kwargs):
#     serializer = LaboratorioSerializer(kwargs['instance'])
#     data = serializer.data
#     update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=Post)
def post_update_signal(sender, **kwargs):
    serializer = PostExportSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


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
