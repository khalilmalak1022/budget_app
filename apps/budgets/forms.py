from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['categorie', 'montant_limite', 'periode']
        widgets = {
            'periode': forms.DateInput(attrs={'type': 'date'}),
        }