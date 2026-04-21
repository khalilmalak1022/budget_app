from django import forms
from .models import Transaction, Categorie

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['montant', 'description', 'date', 'type', 'categorie',
                  'est_recurrente', 'frequence']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'montant': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'couleur', 'icone']
        widgets = {
            'couleur': forms.TextInput(attrs={'type': 'color'}),
        }