from django import forms
from .models import Objectif, Budget, Categorie
from django.utils import timezone

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = Objectif
        fields = ['nom', 'montant_cible', 'date_limite', 'type']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Épargne vacances'
            }),
            'montant_cible': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant en DH',
                'min': '1',
                'step': '0.01'
            }),
            'date_limite': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'nom':           'Nom de l\'objectif',
            'montant_cible': 'Montant cible (DH)',
            'date_limite':   'Date limite',
            'type':          'Type d\'objectif',
        }

    def clean_date_limite(self):
        date_limite = self.cleaned_data.get('date_limite')
        if date_limite and date_limite < timezone.now().date():
            raise forms.ValidationError("La date limite doit être dans le futur.")
        return date_limite

    def clean_montant_cible(self):
        montant = self.cleaned_data.get('montant_cible')
        if montant and montant <= 0:
            raise forms.ValidationError("Le montant doit être supérieur à 0.")
        return montant


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['categorie', 'montant_limite', 'periode']
        widgets = {
            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'montant_limite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant limite en DH',
                'min': '1',
                'step': '0.01'
            }),
            'periode': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'categorie':      'Catégorie',
            'montant_limite': 'Montant limite (DH)',
            'periode':        'Période (choisir n\'importe quel jour du mois)',
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afficher seulement les catégories de l'utilisateur connecté
        self.fields['categorie'].queryset = Categorie.objects.filter(user=user)

    def clean_montant_limite(self):
        montant = self.cleaned_data.get('montant_limite')
        if montant and montant <= 0:
            raise forms.ValidationError("Le montant doit être supérieur à 0.")
        return montant