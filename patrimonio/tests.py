from django.test import TestCase
from .models import Departamento, Movimentacao, Bem
from datetime import date

class MovimentacaoTestCase(TestCase):
    def setUp(self):
        # Criação de bens e departamentos para o teste
        departamento1 = Departamento.objects.create(nome="TI")
        departamento2 = Departamento.objects.create(nome="Financeiro")
        bem = Bem.objects.create(nome="Computador", codigo_rfid="123456789",data_aquisicao=date.today(), departamento=departamento1)
        Movimentacao.objects.create(bem=bem, origem=departamento1, destino=departamento2)

    def test_movimentacao_registro(self):
        movimentacao = Movimentacao.objects.first()
        self.assertEqual(movimentacao.origem.nome, "TI")
        self.assertEqual(movimentacao.destino.nome, "Financeiro")
