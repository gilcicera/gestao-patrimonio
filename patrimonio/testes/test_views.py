from django.test import TestCase
from patrimonio.models import Bem, Categoria, Departamento

class CategoriaTestCase(TestCase):
    def setUp(self):
        Categoria.objects.create(nome="Eletrônicos")

    def test_categoria_nome(self):
        categoria = Categoria.objects.get(nome="Eletrônicos")
        self.assertEqual(categoria.nome, "Eletrônicos")


class BemTestCase(TestCase):
    def setUp(self):
        categoria = Categoria.objects.create(nome="Eletrônicos")
        departamento = Departamento.objects.create(nome="TI")
        Bem.objects.create(
            codigo_rfid="123456789",
            nome="Computador",
            categoria=categoria,
            departamento=departamento,
            data_aquisicao="2025-01-01",
            valor=2500.00,
            status_manutencao=False,
        )

    def test_bem_criacao(self):
        bem = Bem.objects.get(codigo_rfid="123456789")
        self.assertEqual(bem.nome, "Computador")
        self.assertEqual(bem.valor, 2500.00)
        self.assertFalse(bem.status_manutencao)

from django.urls import reverse

class DashboardViewTestCase(TestCase):
    def test_dashboard_view_status_code(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

class RFIDViewTestCase(TestCase):
    def setUp(self):
        categoria = Categoria.objects.create(nome="Eletrônicos")
        departamento = Departamento.objects.create(nome="TI")
        Bem.objects.create(
            codigo_rfid="987654321",
            nome="Notebook",
            categoria=categoria,
            departamento=departamento,
        )

    def test_rfid_view_success(self):
        response = self.client.post(reverse("registrar_rfid"), {"codigo_rfid": "987654321"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Notebook")
