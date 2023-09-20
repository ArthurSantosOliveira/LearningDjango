from django.shortcuts import render
  
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Funcionario, Cargo, Salario

def ordenarFuncionarios(request):
    registros = Funcionario.objects.all()
    return render(request, 'mainDataTable.html', {'registros': registros})


def mediaSalarios(request):
    cargos = Cargo.objects.all()
    
    media_por_cargo = {}
    
    for cargo in cargos:
        funcionarios = Funcionario.objects.filter(cargo=cargo)
        
        salarios_funcionarios = []
        
        for funcionario in funcionarios:
            salarios = Salario.objects.filter(funcionario=funcionario)
            for salario in salarios:
                salarios_funcionarios.append(salario.salario)
        
        salario_total = sum(salarios_funcionarios)
        numero_de_funcionarios = len(salarios_funcionarios)
        
        media = salario_total / numero_de_funcionarios if numero_de_funcionarios > 0 else 0
        
        media_por_cargo[cargo] = media
    
    plt.figure(figsize=(15, 5))


    cargos = [str(cargo) for cargo in media_por_cargo.keys()]
    medias = list(media_por_cargo.values())
    plt.bar(cargos, medias)
    plt.xlabel('Cargos')
    plt.ylabel('Média de Salário')
    plt.title('Média de Salário por Cargo')
    
    # Salve o gráfico em um BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.read()).decode()
    return render(request, 'testeGraficos.html', {'media_por_cargo': media_por_cargo, 'image_base64': image_base64})


def generate_pdf(response):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    cargos = Cargo.objects.all()

    for cargo in cargos:
        #adiciona página por cargo
        p.showPage()
        
        #título de acordo com a página
        p.setFontSize(14)
        p.drawString(100, 750, f"Relatório de Funcionários - {cargo.cargo}")
        p.setLineWidth(1)
        p.line(100, 740, 500, 740)

      
        funcionarios = Funcionario.objects.filter(cargo=cargo)

        # posições da coluna
        x1, x2, x3, y = 100, 250, 400, 700

        # detalhes dos funcionários nas colunas
        p.setFont("Helvetica", 12)
        for funcionario in funcionarios:
            p.drawString(x1, y, f"Nome: {funcionario.nome}")
            p.drawString(x2, y, f"Matrícula: {funcionario.matricula}")
            p.drawString(x3, y, f"Data: {funcionario.data}")
            y -= 20

    # salva o pdf
    p.save()

    buffer.seek(0)
    response.write(buffer.read())

def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_funcionarios.pdf"'

    generate_pdf(response)

    return response