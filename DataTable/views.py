from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import QueryDict
from .models import Funcionario
from django.core.paginator import Paginator
from .forms import BuscaForm, OrdenacaoForm

def mainDataTable(request):
    registers = Funcionario.objects.all()
    # Crie uma instância dos formulários
    busca_form = BuscaForm()  
    ordenacao_form = OrdenacaoForm()
    if request.GET.get('termo_busca'):
        termo_busca = request.GET['termo_busca']
        registers = registers.filter(nome=termo_busca)

    return render(request, 'mainDataTable.html', {'registers': registers, 'busca_form': busca_form,'ordenacao_form': ordenacao_form})

def ordenarFuncionarios(request):
    #obtem valor padrao
    ordenacao = request.GET.get('ordenacao', 'asc')  
    registros = Funcionario.objects.all()

    #ordena os campos de acordo com a escolha
    if ordenacao == 'asc':
        registros = registros.order_by('nome')  
    elif ordenacao == 'desc':
        registros = registros.order_by('-nome') 
    else:
        registros = Funcionario.objects.all()

    termo_busca = request.GET.get('termo_busca', '')
    registros = registros.filter(nome__icontains=termo_busca)

    return render(request, 'mainDataTable.html', {'registers': registros, 'busca_form': BuscaForm({'termo_busca': termo_busca}), 'ordenacao_form': OrdenacaoForm({'ordenacao': ordenacao})})
