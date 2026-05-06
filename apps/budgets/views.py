from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def budget_liste(request):
    return render(request, 'budgets/liste.html')

@login_required
def budget_ajouter(request):
    return render(request, 'budgets/form.html')

@login_required
def budget_modifier(request, pk):
    return render(request, 'budgets/form.html')

@login_required
def budget_supprimer(request, pk):
    return render(request, 'budgets/confirm_delete.html')