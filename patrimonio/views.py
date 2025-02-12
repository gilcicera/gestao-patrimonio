from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Bem, Categoria, Departamento, Movimentacao, Fornecedor
from .forms import BemForm,CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm

def cadastro(request):
    return render(request, 'cadastro.html')
#### TROCAR ASPAS DUPLAS PARA SIMPLESSSS

#views para cadastro
def cadastrar_bem(request):
    if request.method == 'POST':
        form = BemForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo bem no banco de dados
            return redirect('dashboard') 
    else:
        form = BemForm()

    return render(request, 'cadastrar_bem.html', {'form': form})

def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
           # return redirect('dashboard') 
    else:
        form = CategoriaForm()

    return render(request, 'cadastrar_categoria.html', {'form': form})


def cadastrar_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('lista_departamentos')  # Redireciona para a lista de departamentos
    else:
        form = DepartamentoForm()

    return render(request, 'cadastrar_departamento.html', {'form': form})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('lista_departamentos')  # Redireciona para a lista de departamentos
    else:
        form = FornecedorForm()

    return render(request, 'cadastrar_fornecedor.html', {'form': form})

def registrar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_bens')
    else:
        form = MovimentacaoForm()
    return render(request, 'registrar_movimentacao.html', {'form': form})

# views para edição

def editar_bem(request, bem_id):
    bem = get_object_or_404(Bem, id=bem_id)
    if request.method == "POST":
        form = BemForm(request.POST, instance=bem)
        if form.is_valid():
            form.save()
            return redirect('lista_bens')
    else:
        form = BemForm(instance=bem)
    return render(request, 'editar_bem.html', {'form': form})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_bens')  
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form})

def editar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect("lista_bens")
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, "editar_departamento.html", {"form": form})

def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect("lista_bens")
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, "editar_fornecedor.html", {"form": form})


# viewss para excluir
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method in ['POST']:
        categoria.delete()
    return redirect('listar_categorias')

def excluir_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method in ['POST']:
        fornecedor.delete()
    return redirect('listar_fornecedores')

def excluir_departamento(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method in ['POST']:
        departamento.delete()
    return redirect('listar_departamentos')

def excluir_bem(request, pk):
    bem = get_object_or_404(Bem, pk=pk)
    if request.method in ['POST']:
        bem.delete()
    return redirect('listar_bens')



# Dashboard - Exibe os indicadores principais
def dashboard(request):
    total_bens = Bem.objects.count() # Total de bens
    distribuicao_categorias = {categoria.nome: Bem.objects.filter(categoria=categoria).count() for categoria in Categoria.objects.all()} # é uma lista de dicionários para cada categoria
    movimentacoes_recentes = Movimentacao.objects.order_by("-data_movimentacao")[:5] # quer dizer 5 ultimas movimentacoes

    context = { # contexto para a view, o contexto é um dicionário
        "total_bens": total_bens, # Total de bens
        "distribuicao_categorias": distribuicao_categorias, # Dados de distribuição por categoria
        "movimentacoes_recentes": movimentacoes_recentes, # 5 ultimas movimentações
    }
    return render(request, "dashboard.html", context) # renderiza a view dashboard.html com o contexto


# API de Rastreamento RFID - Consulta um bem pelo código RFID
def registrar_rfid(request): # função para registrar o RFID
    if request.method == "POST": 
        codigo_rfid = request.POST.get("codigo_rfid") # pega o código do RFID
        bem = get_object_or_404(Bem, codigo_rfid=codigo_rfid) # busca o bem pelo código RFID
        
        return JsonResponse({ # retorna um JSON com os dados do bem
            "status": "sucesso", # status da operação
            "bem": bem.nome, # nome do bem
            "localizacao": bem.departamento.nome , # localização do bem, que msotra o departamentp e o nome do bem
        })
    
    return JsonResponse({"status": "erro", "mensagem": "Método inválido"}) # se o método não for POST, retorna um erro, e essa mensagem


# Lista de Bens - Página com todos os bens cadastrados
def lista_bens(request):
    bens = Bem.objects.all() # lista de todos os bens
    return render(request, "lista_bens.html", {"bens": bens}) # renderiza a view lista_bens.html com a lista de bens


# Página de detalhes de um bem específico
def detalhe_bem(request, bem_id):
    bem = get_object_or_404(Bem, id=bem_id)
    return render(request, "detalhe_bem.html", {"bem": bem})
