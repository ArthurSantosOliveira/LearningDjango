from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Funcionario
from .models import Funcionario

#teste push e commit via git

def ordenarFuncionarios(request):
    registros = Funcionario.objects.all()
    print('teste')
    return render(request, 'mainDataTable.html', { 'registros':registros})
