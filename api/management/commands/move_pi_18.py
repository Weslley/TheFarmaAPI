from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from api.models.tabela_preco import TabelaPreco
from api.models.uf import Uf


class Command(BaseCommand):
    help = 'Move o piaui para os 18 porcento'
    data = {}

    def handle(self, *args, **options):
        icms_17 = Decimal(17)
        icms_18 = Decimal(18)

        uf = Uf.objects.get(sigla='PI')

        tabelas_17 = TabelaPreco.objects.filter(icms=icms_17)
        tabelas_18 = TabelaPreco.objects.filter(icms=icms_18)

        for tabela in tabelas_17:
            tabela.ufs.remove(uf)
            tabela.data_atualizacao = datetime.now()
            tabela.save()

        for tabela in tabelas_18:
            tabela.ufs.add(uf)
            tabela.data_atualizacao = datetime.now()
            tabela.save()
