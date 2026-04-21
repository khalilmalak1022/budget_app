from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms_auth import RegisterForm
from .models import Profil

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            devise = request.POST.get('devise', 'DH')
            Profil.objects.create(user=user, devise=devise)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects !')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profil(request):
    if request.method == 'POST':
        devise = request.POST.get('devise')
        request.user.profil.devise = devise
        request.user.profil.save()
        messages.success(request, 'Profil mis à jour !')
        return redirect('profil')
    return render(request, 'profil.html')