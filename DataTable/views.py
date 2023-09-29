from django.shortcuts import render
  
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Image,Table, TableStyle

from .models import Funcionario, Cargo, Escritorio

def ordenarFuncionarios(request):

    registros = Funcionario.objects.all()
    cargos = Cargo.objects.all()
    media_por_cargo ={}
    buffer, media_por_cargo = mediaSalarios(request)  

    return render(request, 'mainDataTable.html', {'registros': registros,  'media_por_cargo': media_por_cargo})



def mediaSalarios(request):
    cargos = Cargo.objects.all()

    media_por_cargo = {}

    for cargo in cargos:
        funcionarios = Funcionario.objects.filter(cargo=cargo)

        salarios_funcionarios = []

        for funcionario in funcionarios:
            salario = funcionario.cargo.salario
            if salario is not None:
                salarios_funcionarios.append(salario)

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
    plt.xticks(rotation=0, fontsize=15)
    # Salve o gráfico em um BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    return buffer, media_por_cargo 


def paginaMediaSalarios(request):
    buffer, media_por_cargo = mediaSalarios(request)  
    image_base64 = base64.b64encode(buffer.read()).decode()
    return render(request, 'testeGraficos.html', {'image_base64': image_base64, 'media_por_cargo': media_por_cargo})


def generate_pdf(response, graph_buffer):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    cargos = Cargo.objects.all()
    
    titulo_principal = "Relatório de Funcionários"
    
    p.setFont("Helvetica-Bold", 16)  
    largura_titulo_principal = p.stringWidth(titulo_principal, "Helvetica-Bold", 16)
    x_titulo_principal = (letter[0] - largura_titulo_principal) / 2
    y_titulo_principal = 750
    
    p.drawString(x_titulo_principal, y_titulo_principal, titulo_principal)
    
    p.setLineWidth(1)
    p.line(100, y_titulo_principal - 10, 500, y_titulo_principal - 10)

    imagem = "C:/Users/pesso/Documents/GitHub/LearningDjango/DataTable/static/DataTable/images/tituloCoca.jpeg"
    img = Image(imagem, width=200, height=100)
    img.drawOn(p, 200, 600)

    for cargo in cargos:
        p.showPage()
        p.setFontSize(14)
        p.drawString(100, 750, f"Relatório de Funcionários - {cargo.cargo}")
        p.setLineWidth(1)
        p.line(100, 740, 500, 740)

        imagem = "C:/Users/pesso/Documents/GitHub/LearningDjango/DataTable/static/DataTable/images/logo-coca-cola-brasil.jpg"
        img = Image(imagem, width=200, height=100)
        img.drawOn(p, 400, 750)
      
        funcionarios = Funcionario.objects.filter(cargo=cargo)

        # Crie uma lista de listas para os dados da tabela
        data = [["Nome", "Matrícula", "Data", "Salário"]]
        for funcionario in funcionarios:
            data.append([f"{funcionario.nome} {funcionario.sobrenome}", funcionario.matricula, funcionario.data, cargo.salario])

        # Crie a tabela
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Blacker),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPACEBEFORE', (0, 0), (-1, -1), 12),  
            ('SPACEAFTER', (0, 0), (-1, -1), 12),   
            ('LEFTPADDING', (0, 0), (-1, -1), 12),   
            ('RIGHTPADDING', (0, 0), (-1, -1), 12), 
            ('TOPPADDING', (0, 0), (-1, -1), 12),   
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12) 
        ]))     

        # Adicione a tabela ao PDF
        table.wrapOn(p, 500, 500)
        table.drawOn(p, 150, 650)

    # Adicione a imagem do gráfico ao PDF
    graph_buffer.seek(0)
    img = Image(graph_buffer, width=400, height=200)
    img.drawOn(p, 100, 75)

    # Salva o PDF
    p.save()

    buffer.seek(0)
    response.write(buffer.read())

def funcionarios_por_escritorio(request):
    escritorios = Escritorio.objects.all()

    funcionarios_por_escritorio = {}

    for escritorio in escritorios:
        funcionarios = Funcionario.objects.filter(escritorio=escritorio)
        funcionarios_por_escritorio[escritorio.id] = funcionarios.count()

    # Crie um gráfico de pizza
    labels = [escritorio.cidade for escritorio in escritorios]
    sizes = funcionarios_por_escritorio.values()
    explode = tuple(0.0 for _ in escritorios)  # Espaço entre as fatias do gráfico (opcional)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=100, textprops={'fontsize': 12})
    plt.axis('equal')  # Equal aspect ratio garante que o gráfico seja circular.
    plt.text(0.5, 1.07, "Porcentagem de funcionarios por escritorio", horizontalalignment='center', verticalalignment='center', fontsize=16, transform=plt.gca().transAxes)

    # Salve o gráfico em um BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Crie uma resposta HTTP com o gráfico
    response = HttpResponse(buffer.read(), content_type='image/png')
    return response


def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_funcionarios.pdf"'
    
    graph_buffer, media_por_cargo = mediaSalarios(request) 
    generate_pdf(response, graph_buffer)

    return response
