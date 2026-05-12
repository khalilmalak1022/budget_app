from django import forms

class ExportForm(forms.Form):
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date début'
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date fin'
    )