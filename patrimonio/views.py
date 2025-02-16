from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date, timedelta # timedelta é usado para calcular a data de hoje menos um dia
from .models import Bem, Categoria, Departamento, Movimentacao, Fornecedor
from .forms import BemForm,CategoriaForm, DepartamentoForm, FornecedorForm, MovimentacaoForm

def cadastro(request):
    return render(request, 'cadastro.html')

#views para cadastro

def cadastrar_bem(request):
    departamentos = Departamento.objects.all()  # Busca todos os departamentos
    categorias = Categoria.objects.all()  # Busca todas as categorias
    fornecedores = Fornecedor.objects.all()  # Busca todos os fornecedores

    if request.method == 'POST':
        form = BemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_bens')  # Redirecionar após salvar
    else:
        form = BemForm()

    return render(request, 'cadastrar_bem.html', {
        'form': form,
        'departamentos': departamentos,  # Passando os departamentos
        'categorias': categorias,  # Passando as categorias
        'fornecedores': fornecedores,  # Passando os fornecedores
    })


def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('dashboard') 
    else:
        form = CategoriaForm()

    return render(request, 'cadastrar_categoria.html', {'form': form})


def cadastrar_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redireciona para a lista de departamentos
    else:
        form = DepartamentoForm()

    return render(request, 'cadastrar_departamento.html', {'form': form})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()

    return render(request, 'cadastrar_fornecedor.html', {'form': form})

def registrar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirecione para a página de lista de movimentações ou qualquer outra página.
    else:
        form = MovimentacaoForm()

    bens = Bem.objects.all()
    departamentos = Departamento.objects.all()

    return render(request, 'registrar_movimentacao.html', {'form': form, 'bens': bens, 'departamentos': departamentos})

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


def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)

    return render(request, 'editar_fornecedor.html', {'form': form})



# viewss para excluir
def excluir_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    fornecedor.delete()
    return redirect('lista_fornecedores')

def excluir_bem(request, bem_id):
    bem = get_object_or_404(Bem, id=bem_id)
    if request.method in ['POST']:
        bem.delete()
    return redirect('lista_bens')



# Dashboard - Exibe os indicadores principais
def dashboard(request):
    total_bens = Bem.objects.count() # Total de bens
    distribuicao_categorias = {categoria.nome: Bem.objects.filter(categoria=categoria).count() for categoria in Categoria.objects.all()} # é uma lista de dicionários para cada categoria
    movimentacoes_recentes = Movimentacao.objects.order_by("-data_movimentacao")[:5] # quer dizer 5 ultimas movimentacoes
    valor_total_patrimonio = Bem.objects.aggregate(Sum('valor'))['valor__sum'] or 0 # valor total do patrimonio
    data_limite = date.today() + timedelta(days=7) # Bens próximos da revisão (revisão em até 7 dias)
    bens_proximos_revisao = Bem.objects.filter(data_revisao__lte=data_limite, status_manutencao=False)
    bens_em_manutencao = Bem.objects.filter(status_manutencao=True)

    context = { # contexto para a view, o contexto é um dicionário
        "total_bens": total_bens, # Total de bens
        "distribuicao_categorias": distribuicao_categorias, # Dados de distribuição por categoria
        "movimentacoes_recentes": movimentacoes_recentes, # 5 ultimas movimentações
        "bens_proximos_revisao": bens_proximos_revisao,
        "valor_total_patrimonio": valor_total_patrimonio,
        "bens_em_manutencao": bens_em_manutencao,
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

def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'lista_fornecedores.html', {'fornecedores': fornecedores})


