from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Medicamento


@receiver(post_save, sender=Medicamento)
def teste_signal(sender, **kwargs):
    print('sender')
    print(sender)
    print('kwargs')
    print(kwargs)
