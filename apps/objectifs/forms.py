from django import forms
from .models import Objectif

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = Objectif
        fields = ['nom', 'montant_cible', 'date_limite', 'type']
        widgets = {
            'date_limite': forms.DateInput(attrs={'type': 'date'}),
        }