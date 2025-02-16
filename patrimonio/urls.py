from django.urls import path
from .views import (dashboard, lista_bens, cadastrar_bem, cadastrar_categoria, cadastrar_departamento, cadastrar_fornecedor, cadastro,
                    registrar_movimentacao, editar_bem, excluir_bem, lista_fornecedores, editar_fornecedor, excluir_fornecedor,
                    )

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('cadastro/', cadastro, name='cadastro'),
    # urls para bens
    path('bens/', lista_bens, name='lista_bens'),
    path('bens/editar/<int:bem_id>/', editar_bem, name='editar_bem'),
    path('bens/excluir/<int:bem_id>/', excluir_bem, name='excluir_bem'),

    # urls para fornecedores
    path('fornecedores/', lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/editar/<int:fornecedor_id>/', editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/excluir/<int:fornecedor_id>/', excluir_fornecedor, name='excluir_fornecedor'),

    # urls para cadastro
    path('cadastrar_bem/', cadastrar_bem,  name='cadastrar_bem'),
    path('registrar_movimentacao/', registrar_movimentacao, name='registrar_movimentacao'),
    path('cadastrar_categoria/', cadastrar_categoria,  name='cadastrar_categoria'),
    path('cadastrar_departamento/', cadastrar_departamento,  name='cadastrar_departamento'),
    path('cadastrar_fornecedor/', cadastrar_fornecedor,  name='cadastrar_fornecedor'),
]
