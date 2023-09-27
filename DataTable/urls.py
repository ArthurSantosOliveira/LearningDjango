from django.urls import path
from . import views

urlpatterns = [
    path('ordenarFuncionarios/', views.ordenarFuncionarios, name='ordenarFuncionarios'),
    path('mediaSalarios/', views.mediaSalarios, name='mediaSalarios'),
    path('gerarPDFs/', views.pdf_view, name='gerarPDFs'),  
    path('paginaMediaSalarios/', views.paginaMediaSalarios, name='paginaMediaSalarios'),
    path('gerar_grafico_pizza/', views.funcionarios_por_escritorio, name='gerar_grafico_pizza'),
]