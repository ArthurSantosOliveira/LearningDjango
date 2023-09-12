from django.db import models

# Create your models here.
class Funcionario(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField()
    cargo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=250)
    valor_base = models.DecimalField(max_digits=10, decimal_places=2)
    proventos = models.DecimalField(max_digits=10, decimal_places=2)
    descontos = models.DecimalField(max_digits=10, decimal_places=2)
    liquidos = models.DecimalField(max_digits=10, decimal_places=2)
    
