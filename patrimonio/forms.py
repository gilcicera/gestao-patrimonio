from django import forms
from .models import Bem, Categoria, Departamento, Fornecedor, Movimentacao

class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = ['nome', 'codigo_rfid', 'categoria', 'departamento','fornecedor', 'data_aquisicao', 'valor', 'status_manutencao']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome']

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'contato']

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ["bem", "origem", "destino"]