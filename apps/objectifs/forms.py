from django import forms
from .models import Objectif


class ObjectifForm(forms.ModelForm):
    class Meta:
        model  = Objectif
        fields = ['nom', 'type', 'montant_cible', 'date_limite', 'description']
        widgets = {
            'nom':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Vacances été 2025'}),
            'type':          forms.Select(attrs={'class': 'form-select'}),
            'montant_cible': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'date_limite':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description':   forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description optionnelle…'}),
        }
        labels = {
            'nom':           "Nom de l'objectif",
            'type':          "Type d'objectif",
            'montant_cible': 'Montant cible (DH)',
            'date_limite':   'Date limite',
            'description':   'Description',
        }