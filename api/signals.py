from django.db.models.signals import post_save
from django.dispatch import receiver
from pyrebase import pyrebase
from django.conf import settings
from api.models import *
from api.serializers import *


def update_model(model_name, data):
    try:
        firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
        auth = firebase.auth()
        user = auth.current_user
        db = firebase.database()
        table = '{}s'.format(model_name)
        row = '{0}_{1}'.format(model_name, data['id'])
        db.child(table).child(row).set(data)
    except:
        pass


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


@receiver(post_save, sender=GrupoMedicamento)
def grupo_medicamento_update_signal(sender, **kwargs):
    serializer = GrupoMedicamentoSerializer(kwargs['instance'])
    data = serializer.data
    update_model(sender.__name__.lower(), data)