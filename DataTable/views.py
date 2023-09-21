from django.shortcuts import render
  
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

from .models import Funcionario, Cargo, Salario

def ordenarFuncionarios(request):
    registros = Funcionario.objects.all()
    return render(request, 'mainDataTable.html', {'registros': registros})


# ...

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
    
    # Ajusta tamanho e a fonte 
    p.setFont("Helvetica-Bold", 16)  
    
    # Centraliza o título 
    largura_titulo_principal = p.stringWidth(titulo_principal, "Helvetica-Bold", 16)
    x_titulo_principal = (letter[0] - largura_titulo_principal) / 2
    
    # Ajusta a posição vertical 
    y_titulo_principal = 750
    
    # Desenha o título no PDF
    p.drawString(x_titulo_principal, y_titulo_principal, titulo_principal)
    
    p.setLineWidth(1)
    p.line(100, y_titulo_principal - 10, 500, y_titulo_principal - 10)

    imagem = "C:/Users/pesso/OneDrive/Documentos/GitHub/LearningDjango/DataTable/static/images/tituloCoca.jpeg"
    img = Image(imagem, width=200, height=100)
    img.drawOn(p, 200, 600)

    for cargo in cargos:
        # Adiciona página por cargo
        p.showPage()
        
        # Título de acordo com a página
        p.setFontSize(14)
        p.drawString(100, 750, f"Relatório de Funcionários - {cargo.cargo}")
        p.setLineWidth(1)
        p.line(100, 740, 500, 740)

        # Se eu colocar a imagem aqui ela vai aparecer em todas as páginas (pode ser útil para uma logotipo ou marca d'água)
        imagem = "C:/Users/pesso/OneDrive/Documentos/GitHub/LearningDjango/DataTable/static/images/logoCoca.png"
        img = Image(imagem, width=200, height=100)
        img.drawOn(p, 400, 750)
      
        funcionarios = Funcionario.objects.filter(cargo=cargo)

        # Posições da coluna para A4
        x1, x2, x3 ,y = 100, 250, 400, 700

        # Detalhes dos funcionários nas colunas
        p.setFont("Helvetica", 12)
        for funcionario in funcionarios:
            p.drawString(x1, y, f"Nome: {funcionario.nome}")
            p.drawString(x2, y, f"Matrícula: {funcionario.matricula}")
            p.drawString(x3, y, f"Data: {funcionario.data}")

            y -= 20

    # Adicione a imagem do gráfico ao PDF
    graph_buffer.seek(0)
    img = Image(graph_buffer, width=400, height=200)
    img.drawOn(p, 100, 75)

    # Salva o PDF
    p.save()

    buffer.seek(0)
    response.write(buffer.read())


def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_funcionarios.pdf"'
    
    graph_buffer = mediaSalarios(request)
    generate_pdf(response, graph_buffer)

    return response