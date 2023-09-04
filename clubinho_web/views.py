from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
import requests

from .models import Cliente
from .forms import ClienteForm

def main(request):
    return render(request, 'main.html')

def create_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = ClienteForm()
    return render(request, 'create_cliente.html', {'form': form})

def read_cliente(request):
    mymembers = Cliente.objects.all()
    return render(request, 'read_cliente.html', {'mymembers': mymembers})

def details(request, id):
    mymember = Cliente.objects.get(id=id)
    return render(request, 'details.html', {'mymember': mymember})


def update_cliente(request, id):
    mymember = Cliente.objects.get(id=id)
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('main')  # Redirecionar para onde você desejar
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'update_cliente.html', {'form': form ,'mymember': mymember})


def processa_formulario(request):
    form = ClienteForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('main')
    return HttpResponse("ERRO")

def api_test(request):
    api_url = 'https://api.adviceslip.com/advice'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()  # Converte a resposta JSON em um dicionário Python
    else:
        data = {}  # Lidar com erros, se necessário
    return render(request, 'api_test.html', {'data': data})

def reload_advices(request):
    return render(request, 'api_test.html')
