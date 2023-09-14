from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode

from DataTable.models import Funcionario, Salario, Cargo

class FuncionarioAdminForm(forms.ModelForm):
    class Meta: 
        model = Funcionario
        fields = "__all__"

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "data", "matricula", "exibir_salario")
    search_fields = ("nome", "matricula")

    def exibir_salario(self, obj):
        salario = Salario.objects.filter(funcionario=obj).last()
        if salario:
            return salario.salario
        return "Nenhum registro de salário"

    exibir_salario.short_description = "Salário"

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("cargo", "nivel")

@admin.register(Salario)
class SalarioAdmin(admin.ModelAdmin):
    list_display = ("salario", "funcionario")
