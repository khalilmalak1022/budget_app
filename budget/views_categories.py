from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categorie
from .forms_transactions import CategorieForm

@login_required
def categorie_liste(request):
    categories = Categorie.objects.filter(user=request.user)
    return render(request, 'categories/liste.html',
        {'categories': categories})

@login_required
def categorie_ajouter(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            categorie = form.save(commit=False)
            categorie.user = request.user
            categorie.save()
            messages.success(request, 'Catégorie ajoutée !')
            return redirect('categorie_liste')
    else:
        form = CategorieForm()
    return render(request, 'categories/form.html', {'form': form})

@login_required
def categorie_modifier(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie modifiée !')
            return redirect('categorie_liste')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'categories/form.html', {'form': form})

@login_required
def categorie_supprimer(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk, user=request.user)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée !')
        return redirect('categorie_liste')
    return render(request, 'categories/confirm_delete.html',
        {'obj': categorie})