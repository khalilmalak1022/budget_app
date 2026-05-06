from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def objectif_liste(request):
    return render(request, 'objectifs/liste.html')

@login_required
def objectif_ajouter(request):
    return render(request, 'objectifs/form.html')

@login_required
def objectif_modifier(request, pk):
    return render(request, 'objectifs/form.html')

@login_required
def objectif_supprimer(request, pk):
    return render(request, 'objectifs/confirm_delete.html')