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



def distribuidoras_count(obj):
    return obj.distribuidoras_count
def distribuidora_lista(obj):
    return ", ".join([str(d.nome_fantasia) for d in obj.distribuidoras.all()])


@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'cpf', 'distribuidoras_count', 'distribuidoras_list')

    def distribuidoras_count(self, obj):
        return obj.distribuidoras.count()
    
    distribuidoras_count.short_description = 'Quantidade de Distribuidoras'

    def distribuidoras_list(self, obj):
        return ", ".join([str(d.nome_fantasia) for d in obj.distribuidoras.all()])

    distribuidoras_list.short_description = 'Distribuidoras Relacionadas'

    ordering = ('-id',)  

    def distribuidoras_list_reverse(self, obj):
        return ", ".join([str(d.nome_fantasia) for d in obj.distribuidoras.all()])

    distribuidoras_list_reverse.short_description = 'Distribuidoras (reverso)'

    list_display_links = ('nome', 'sobrenome')


    

@admin.register(Distribuidora)
class DistribuidoraAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'endereco', 'cnpj', 'cep', 'proprietario', 'exibir_valor_total_pedidos')

    def exibir_valor_total_pedidos(self, obj):
        return obj.calcular_valor_total_pedidos()

    exibir_valor_total_pedidos.short_description = 'Valor Total de Pedidos'


    
@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_und')

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantidade', 'data_pedido')

@admin.register(RegistroPedido)
class RegistroPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'pedido', 'quantidade', 'valor_total', 'distribuidora_do_pedido')

    def valor_total(self, obj):
        return obj.produto.preco_und * obj.quantidade

    valor_total.short_description = 'Valor Total do Pedido'
    
    def distribuidora_do_pedido(self, obj):
        if obj.pedido:
            return obj.pedido.distribuidora.nome_fantasia if obj.pedido.distribuidora else "N/A"
        return "N/A"