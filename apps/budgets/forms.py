from django import forms
from .models import Budget
from apps.transactions.models import Categorie


class BudgetForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = Categorie.objects.filter(user=user)
        self.fields['categorie'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model   = Budget
        fields  = ['categorie', 'montant_limite', 'periode']
        widgets = {
            'montant_limite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'periode':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'categorie':      'Catégorie',
            'montant_limite': 'Montant limite (DH)',
            'periode':        'Mois concerné (choisir le 1er du mois)',
        }