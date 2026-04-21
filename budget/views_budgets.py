from django.contrib.auth.decorators import login_required

@login_required
def budget_liste(request): pass
@login_required
def budget_ajouter(request): pass
@login_required
def budget_modifier(request, pk): pass
@login_required
def budget_supprimer(request, pk): pass