from django.db.models.signals import post_save
from django.dispatch import receiver
from pyrebase import pyrebase
from django.conf import settings

from api.models.cidade import Cidade
from api.models.farmacia import Farmacia
from api.models.laboratorio import Laboratorio
from api.models.medicamento import Medicamento
from api.models.principio_ativo import PrincipioAtivo
from api.serializers.cidade import CidadeSerializer
from api.serializers.farmacia import FarmaciaSerializer
from api.serializers.laboratorio import LaboratorioSerializer
from api.serializers.medicamento import MedicamentoSerializer
from api.serializers.principio_ativo import PrincipioAtivoSerializer


def update_model(model_name, data):
    try:
        firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
        auth = firebase.auth()
        user = auth.current_user
        db = firebase.database()
        table = '{}s'.format(model_name)
        row = '{0}_{1}'.format(model_name, data['id'])
        db.child(table).child(row).remove()
    except Exception as err:
        print(err)


@receiver(post_save, sender=Medicamento)
def teste_signal(sender, **kwargs):
    serializer = MedicamentoSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=Medicamento)
def medicamento_update_signal(sender, **kwargs):
    serializer = MedicamentoSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=Farmacia)
def farmacia_update_signal(sender, **kwargs):
    serializer = FarmaciaSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=Cidade)
def cidade_update_signal(sender, **kwargs):
    serializer = CidadeSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=PrincipioAtivo)
def principio_ativo_update_signal(sender, **kwargs):
    serializer = PrincipioAtivoSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)


@receiver(post_save, sender=Laboratorio)
def laboratorio_update_signal(sender, **kwargs):
    serializer = LaboratorioSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)
