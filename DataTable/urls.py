from django.urls import path
from . import views

urlpatterns = [
    path('ordenarFuncionarios/', views.ordenarFuncionarios, name='ordenarFuncionarios'),

]