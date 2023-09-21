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