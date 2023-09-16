from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Funcionario
from .models import Funcionario



def ordenarFuncionarios(request):
    registros = Funcionario.objects.all()

    return render(request, 'mainDataTable.html', { 'registros':registros})
