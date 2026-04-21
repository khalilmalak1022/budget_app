from django.contrib.auth.decorators import login_required

@login_required
def objectif_liste(request): pass
@login_required
def objectif_ajouter(request): pass
@login_required
def objectif_modifier(request, pk): pass
@login_required
def objectif_supprimer(request, pk): pass