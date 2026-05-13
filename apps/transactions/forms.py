from django import forms
from .models import Transaction, Categorie

COULEURS = [
    ('#e74c3c', 'Rouge'),
    ('#e67e22', 'Orange'),
    ('#f1c40f', 'Jaune'),
    ('#2ecc71', 'Vert'),
    ('#1abc9c', 'Turquoise'),
    ('#3498db', 'Bleu'),
    ('#9b59b6', 'Violet'),
    ('#e91e63', 'Rose'),
    ('#795548', 'Marron'),
    ('#607d8b', 'Gris'),
]

ICONES = [
    ('bi bi-cart', 'Courses'),
    ('bi bi-house', 'Logement'),
    ('bi bi-car-front', 'Transport'),
    ('bi bi-lightning', 'Electricite'),
    ('bi bi-heart-pulse', 'Sante'),
    ('bi bi-controller', 'Loisirs'),
    ('bi bi-book', 'Education'),
    ('bi bi-bag', 'Vetements'),
    ('bi bi-phone', 'Telephone'),
    ('bi bi-cash-coin', 'Salaire'),
]

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
    couleur = forms.ChoiceField(
        choices=COULEURS,
        initial='#3498db'
    )
    icone = forms.ChoiceField(
        choices=ICONES,
        required=False
    )

    class Meta:
        model = Categorie
        fields = ['nom', 'couleur', 'icone']
