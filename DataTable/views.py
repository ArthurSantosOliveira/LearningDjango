from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse  # Import HttpResponse for rendering the chart

from .models import Funcionario


def ordenarFuncionarios(request):
    registros = Funcionario.objects.all()
    return render(request, 'mainDataTable.html', {'registros': registros})



