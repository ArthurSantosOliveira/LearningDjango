# forms.py
from django import forms

class BuscaForm(forms.Form):
    termo_busca = forms.CharField(max_length=100, label='Pesquisar', required=False)

class  OrdenacaoForm(forms.Form):
    escolhas = [
        ('all', ''),
        ('asc', 'Nome (A-Z)'),
        ('desc', 'Nome (Z-A)'),
    ]
    ordenacao = forms.ChoiceField(choices=escolhas, label='Ordenar por')
