import inspect

import sys

import pyrebase

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models.apresentacao import Apresentacao
from api.models.fabricante import Fabricante
from api.models.produto import Produto
from api.models.principio_ativo import PrincipioAtivo
from api.models.tabela_preco import TabelaPreco
from api.serializers.apresentacao import ApresentacaoExportSerializer
from api.serializers.laboratorio import LaboratorioSerializer
from api.serializers.medicamento import *
from api.serializers.principio_ativo import PrincipioAtivoSerializer
from api.serializers.tabela_preco import TabelaPrecoSerializer


class Command(BaseCommand):
    help = 'Comando para exporta dados dos medicamento do Banco para o FIrebase'
    data = {}

    def handle(self, *args, **options):
        for method_name in self.get_methods():
            method = getattr(self, method_name)
            method()
            key = list(self.data.keys())[0]
            data = self.data[key]
            firebase = pyrebase.initialize_app(settings.PYREBASE_CONFIG)
            auth = firebase.auth()
            user = auth.current_user
            db = firebase.database()
            print('Upload...')
            db.child(key).set(data)
            self.data = {}

    def eaxport_medicamento(self):
        medicamentos = {}
        spinner = spinning_cursor()
        print('Carregando medicamentos...')
        for medicamento in Produto.objects.all():
            serializer = MedicamentoExportSerializer(medicamento)
            data = serializer.data
            medicamentos[data['id']] = data
            print_spinner(spinner)
        self.data['medicamentos'] = medicamentos
        print('Medicamentos... OK')

    def exaport_apresentacoes(self):
        apresentacoes = {}
        spinner = spinning_cursor()
        print('Carregando apesentações...')
        for apresentacao in Apresentacao.objects.all():
            serializer = ApresentacaoExportSerializer(apresentacao)
            data = serializer.data
            apresentacoes[data['id']] = data
            print_spinner(spinner)
        self.data['apresentacoes'] = apresentacoes
        print('Apresentações... OK')

    def exporat_tabela_preco(self):
        tabelas = {}
        spinner = spinning_cursor()
        print('Carregando tabelas de preço...')
        for tabela in TabelaPreco.objects.all():
            serializer = TabelaPrecoSerializer(tabela)
            data = serializer.data
            tabelas[data['id']] = data
            print_spinner(spinner)
        self.data['tabelas_preco'] = tabelas
        print('Tabela de preços... OK')

    def export_laboratorio(self):
        laboratorios = {}
        spinner = spinning_cursor()
        print('Carregando laboratórios...')
        for lab in Fabricante.objects.all():
            serializer = LaboratorioSerializer(lab)
            data = serializer.data
            laboratorios[data['id']] = data
            print_spinner(spinner)
        self.data['laboratorios'] = laboratorios
        print('Laboratórios... OK')

    def export_principio_ativo(self):
        principios = {}
        spinner = spinning_cursor()
        print('Carregando princípios ativos...')
        for principio in PrincipioAtivo.objects.all():
            serializer = PrincipioAtivoSerializer(principio)
            data = serializer.data
            principios[data['id']] = data
            print_spinner(spinner)
        self.data['principios_ativos'] = principios
        print('Princípios ativos... OK')

    def get_methods(self):
        return [t[0] for t in inspect.getmembers(self, inspect.ismethod) if t[0].startswith('export_')]


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def print_spinner(spinner):
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    sys.stdout.write('\b')
