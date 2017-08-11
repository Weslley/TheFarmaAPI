from datetime import datetime

from django.db.models import Q
from django.core.management.base import BaseCommand

from api.models.apresentacao import Apresentacao


class Command(BaseCommand):
    data = {}

    def handle(self, *args, **options):
        apresentacoes = Apresentacao.objects.filter(
            Q(codigo_barras__isnull=True) | Q(codigo_barras=0),
            ativo=True,
        )
        print("{} apresentações...".format(apresentacoes.count()))
        for apresentacao in apresentacoes:
            apresentacao.ativo = False
            apresentacao.data_atualizacao = datetime.now()
            apresentacao.save()
