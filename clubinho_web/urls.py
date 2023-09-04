from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('create_cliente/', views.create_cliente, name='create_cliente'),
    path('processa_formulario/', views.processa_formulario, name="processa_formulario"),
    path('read_cliente/', views.read_cliente, name="read_cliente"),
    path('details/update_cliente/<int:id>/', views.update_cliente, name='update_cliente'),
    path('read_cliente/details/<int:id>/', views.details, name='details'),
    path('reload_advices/', views.api_test, name = "api_test"),
]
