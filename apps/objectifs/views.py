from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date

from .models import Objectif
from .forms import ObjectifForm
from apps.transactions.models import Transaction


@login_required
def objectif_liste(request):
    objectifs = Objectif.objects.filter(user=request.user)
    today     = date.today()
    objectifs_data = []

    for obj in objectifs:
        if obj.type == 'epargne':
            montant_actuel = Transaction.objects.filter(
                user=request.user, type='revenu', date__lte=today
            ).aggregate(total=Sum('montant'))['total'] or 0
        else:
            montant_actuel = Transaction.objects.filter(
                user=request.user, type='depense',
                date__month=today.month, date__year=today.year
            ).aggregate(total=Sum('montant'))['total'] or 0

        pourcentage = min(int((float(montant_actuel) / float(obj.montant_cible)) * 100), 100) if obj.montant_cible > 0 else 0

        if obj.type == 'limite':
            couleur = 'danger' if pourcentage >= 100 else 'warning' if pourcentage >= 75 else 'success'
        else:
            couleur = 'success' if pourcentage >= 100 else 'info' if pourcentage >= 50 else 'warning'

        objectifs_data.append({
            'objectif':       obj,
            'montant_actuel': montant_actuel,
            'pourcentage':    pourcentage,
            'couleur':        couleur,
            'jours_restants': (obj.date_limite - today).days,
            'depasse':        obj.type == 'limite' and float(montant_actuel) > float(obj.montant_cible),
            'atteint':        obj.type == 'epargne' and float(montant_actuel) >= float(obj.montant_cible),
        })

    return render(request, 'objectifs/liste.html', {'objectifs_data': objectifs_data})


@login_required
def objectif_ajouter(request):
    form = ObjectifForm(request.POST or None)
    if form.is_valid():
        o = form.save(commit=False)
        o.user = request.user
        o.save()
        messages.success(request, "Objectif ajouté avec succès !")
        return redirect('objectif_liste')
    return render(request, 'objectifs/form.html', {'form': form, 'titre': 'Nouvel objectif'})


@login_required
def objectif_modifier(request, pk):
    objectif = get_object_or_404(Objectif, pk=pk, user=request.user)
    form = ObjectifForm(request.POST or None, instance=objectif)
    if form.is_valid():
        form.save()
        messages.success(request, "Objectif modifié avec succès !")
        return redirect('objectif_liste')
    return render(request, 'objectifs/form.html', {'form': form, 'titre': "Modifier l'objectif"})


@login_required
def objectif_supprimer(request, pk):
    objectif = get_object_or_404(Objectif, pk=pk, user=request.user)
    if request.method == 'POST':
        objectif.delete()
        messages.success(request, "Objectif supprimé.")
        return redirect('objectif_liste')
    return render(request, 'objectifs/confirm_delete.html', {
        'objet':   objectif,
        'titre':   "Supprimer l'objectif",
        'message': f'Voulez-vous vraiment supprimer "{objectif.nom}" ?',
        'retour':  'objectif_liste',
    })