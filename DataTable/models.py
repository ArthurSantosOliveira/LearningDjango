from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Cargo(models.Model):
    cargo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=250)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    def __str__(self):
        return self.cargo


class Funcionario(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField()

    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Funcionarios"

class FuncionarioCargo(models.Model):
    id_funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    inicio = models.DateField()
    fim = models.DateField(null=True, blank=True)

    def clean(self):
        if self.fim and self.inicio > self.fim:
            raise ValidationError("A data de início não pode ser posterior à data de término.")

    def __str__(self):
        return f"{self.id_funcionario} - {self.id_cargo} ({self.inicio} to {self.fim})"





class Proprietario(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    # Validador do CPF
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class Distribuidora(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    endereco = models.CharField(max_length=300)
    # Validador do CNPJ
    cnpj = models.CharField(max_length=18, unique=True)
    cep = models.CharField(max_length=9)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE, related_name='distribuidoras')
    
    def __str__(self):
        return self.nome_fantasia
    
    def calcular_valor_total_pedidos(self):
        total = 0.0
        for pedido in self.pedidos.all():
            for registro in pedido.registropedido_set.all():
                total += registro.quantidade * registro.produto.preco_und
        return total

class Produtos(models.Model):
    nome = models.CharField(max_length=100)
    preco_und = models.FloatField()

    def __str__(self):
        return self.nome

class Pedidos(models.Model):
    quantidade = models.PositiveIntegerField()
    data_pedido = models.DateField()
    produtos = models.ManyToManyField(Produtos, related_name='pedidos', through='RegistroPedido')
    distribuidora = models.ForeignKey(Distribuidora, on_delete=models.CASCADE, related_name='pedidos') 

    def __str__(self):
        return f"Pedido {self.id}"

class RegistroPedido(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"Registro de Pedido {self.id}"
