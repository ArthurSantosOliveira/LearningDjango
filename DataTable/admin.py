from django import forms
from django.contrib import admin
from django.db.models import Count
from django.core.exceptions import ValidationError

from .models import Funcionario, Cargo, FuncionarioCargo, Proprietario, Distribuidora, Produtos, Pedidos, RegistroPedido

class FuncionarioAdminForm(forms.ModelForm):
    class Meta: 
        model = Funcionario
        fields = "__all__"

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "data", "matricula", "mostrar_salario")
    search_fields = ("nome", "matricula")

    def mostrar_salario(self, obj):
        funcionario_cargo = FuncionarioCargo.objects.filter(id_funcionario=obj).last()
        if funcionario_cargo:
            return funcionario_cargo.id_cargo.salario
        return "Nenhum registro de salário"

    mostrar_salario.short_description = "Salário"

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("cargo", "nivel", "salario")

@admin.register(FuncionarioCargo)
class FuncionarioCargoAdmin(admin.ModelAdmin):
    list_display = ("id_funcionario", "id_cargo", "inicio", "fim")
    search_fields = ("id_funcionario__nome", "id_cargo__cargo")

    def clean(self):
        if self.fim and self.inicio > self.fim:
            raise ValidationError("A data de início não pode ser posterior à data de término.")




    
