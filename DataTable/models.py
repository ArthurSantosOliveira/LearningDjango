from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Cargo(models.Model):
    cargo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=250)
    
    def __str__(self):
        return self.cargo


# Create your models here.
class Funcionario(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField()
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Funcionarios"

class Salario(models.Model):
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='salarios', null=True)

    def __str__(self):
        return str(self.salario)
