from django.test import TestCase
from api.servico_pagamento.pagamento import Pagamento, ServicoNaoImplementado
from api.servico_pagamento import tipo_servicos


class TestPagamento(TestCase):

    def setUp(self):
        self.data = {}

    def test_pagamento_cielo(self):
        self.assertTrue(Pagamento.pagar(tipo_servicos.CIELO, **self.data), "Pagamento retorna True")

    def test_pagamento_nao_implementado(self):
        with self.assertRaises(ServicoNaoImplementado):
            Pagamento.pagar(tipo_servicos.NAO_IMPLEMENTADO, **self.data)
