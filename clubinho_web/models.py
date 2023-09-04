from django.db import models
# Create your models here.

class Cliente(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    

    def __str__(self):
        return f"{self.name} {self.last_name}"
