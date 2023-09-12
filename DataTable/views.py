from django.shortcuts import render
from .models import Funcionario
from django.core.paginator import Paginator

# Create your views here.
def mainDataTable(request):
    registers = Funcionario.objects.all()
    return render(request, 'mainDataTable.html', {'registers': registers})

