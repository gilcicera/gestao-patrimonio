from django import forms
from .models import Bem, Categoria, Departamento, Fornecedor, Movimentacao

class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = "__all__"

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