from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    devise = forms.ChoiceField(
        choices=[('DH','Dirham (DH)'),('EUR','Euro (€)'),('USD','Dollar ($)')],
        initial='DH'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'devise']