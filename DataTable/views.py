from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Funcionario
from .forms import BuscaForm, OrdenacaoForm

def mainDataTable(request):
    # registros de Funcionario
    registros = Funcionario.objects.all()

    # instância dos formulários
    busca_form = BuscaForm()
    ordenacao_form = OrdenacaoForm()

    # número de registros a serem exibidos por página
    registros_por_pagina = 10
    paginator = Paginator(registros, registros_por_pagina)
    pagina_numero = request.GET.get('page')
    pagina_atual = paginator.get_page(pagina_numero)

    # pesquisa
    termo_busca = request.GET.get('termo_busca')
    if termo_busca:
        registros = registros.filter(nome__icontains=termo_busca)

    return render(request, 'mainDataTable.html', {'pagina_atual': pagina_atual, 'busca_form': busca_form, 'ordenacao_form': ordenacao_form})

def ordenarFuncionarios(request):
    # pega o valor do GET
    ordenacao = request.GET.get('ordenacao', 'asc')
    termo_busca = request.GET.get('termo_busca', '')

    registros = Funcionario.objects.all()

    # ordena os registros
    if ordenacao == 'asc':
        registros = registros.order_by('nome')
    elif ordenacao == 'desc':
        registros = registros.order_by('-nome')

    # filtra os registros
    registros = registros.filter(nome__icontains=termo_busca)

    # número de registros a serem exibidos por página
    registros_por_pagina = 10
    paginator = Paginator(registros, registros_por_pagina)
    pagina_numero = request.GET.get('page')
    pagina_atual = paginator.get_page(pagina_numero)

    return render(request, 'mainDataTable.html', {'pagina_atual': pagina_atual, 'busca_form': BuscaForm({'termo_busca': termo_busca}), 'ordenacao_form': OrdenacaoForm({'ordenacao': ordenacao})})
