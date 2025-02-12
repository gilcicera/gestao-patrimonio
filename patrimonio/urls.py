from django.urls import path
from .views import (dashboard, lista_bens, detalhe_bem, cadastrar_bem, cadastrar_categoria, cadastrar_departamento, cadastrar_fornecedor, cadastro,
                    registrar_movimentacao, editar_bem, excluir_bem)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('cadastro/', cadastro, name='cadastro'),

    path('bens/', lista_bens, name='lista_bens'),
    path("bens/<int:bem_id>/", detalhe_bem, name="detalhe_bem"),
    # urls para cadastro
    path('cadastrar_bem/', cadastrar_bem,  name= 'cadastrar_bem'),
    path('registrar_movimentacao/', registrar_movimentacao, name='registrar_movimentacao'),
    path('bens/editar/<int:bem_id>/', editar_bem, name='editar_bem'),
    path('bens/excluir/<int:bem_id>/', excluir_bem, name='excluir_bem'),
    path('cadastrar_categoria/', cadastrar_categoria,  name= 'cadastrar_categoria'),
    path('cadastrar_departamento/', cadastrar_departamento,  name= 'cadastrar_departamento'),
    path('cadastrar_fornecedor/', cadastrar_fornecedor,  name= 'cadastrar_fornecedor'),
]
