from django.urls import path
from . import views

urlpatterns = [
    path('ordenarFuncionarios/', views.ordenarFuncionarios, name='ordenarFuncionarios'),
    path('mediaSalarios/', views.mediaSalarios, name='mediaSalarios'),
    path('gerarPDFs/', views.pdf_view, name='gerarPDFs'),  
    #path('pdf_view', views.pdf_view, name='pdf_view'),

]