from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from .models import Objectif, Budget, Transaction
from .forms_objectifs import ObjectifForm, BudgetForm


# ═══════════════════════════════════════════════════════
#  OBJECTIFS
# ═══════════════════════════════════════════════════════

@login_required
def objectif_liste(request):
    objectifs = Objectif.objects.filter(user=request.user)
    today = date.today()

    objectifs_data = []
    for obj in objectifs:

        # Calcul de la progression selon le type
        if obj.type == 'epargne':
            # Total des revenus depuis la création jusqu'à la date limite
            montant_actuel = Transaction.objects.filter(
                user=request.user,
                type='revenu',
                date__lte=today
            ).aggregate(total=Sum('montant'))['total'] or 0

        else:  # limite de dépenses
            # Total des dépenses du mois en cours
            montant_actuel = Transaction.objects.filter(
                user=request.user,
                type='depense',
                date__month=today.month,
                date__year=today.year
            ).aggregate(total=Sum('montant'))['total'] or 0

        # Calcul pourcentage
        if obj.montant_cible > 0:
            pourcentage = min(int((float(montant_actuel) / float(obj.montant_cible)) * 100), 100)
        else:
            pourcentage = 0

        # Couleur de la barre
        if obj.type == 'limite':
            if pourcentage >= 100:
                couleur = 'danger'   # rouge — dépassé
            elif pourcentage >= 75:
                couleur = 'warning'  # orange — proche
            else:
                couleur = 'success'  # vert — ok
        else:
            if pourcentage >= 100:
                couleur = 'success'  # vert — objectif atteint
            elif pourcentage >= 50:
                couleur = 'info'     # bleu — en bonne voie
            else:
                couleur = 'warning'  # orange — à améliorer

        # Jours restants
        jours_restants = (obj.date_limite - today).days

        objectifs_data.append({
            'objectif':       obj,
            'montant_actuel': montant_actuel,
            'pourcentage':    pourcentage,
            'couleur':        couleur,
            'jours_restants': jours_restants,
            'depasse':        obj.type == 'limite' and float(montant_actuel) > float(obj.montant_cible),
        })

    return render(request, 'objectifs/liste.html', {
        'objectifs_data': objectifs_data,
    })


@login_required
def objectif_ajouter(request):
    if request.method == 'POST':
        form = ObjectifForm(request.POST)
        if form.is_valid():
            objectif = form.save(commit=False)
            objectif.user = request.user
            objectif.save()
            messages.success(request, "Objectif ajouté avec succès !")
            return redirect('objectif_liste')
    else:
        form = ObjectifForm()

    return render(request, 'objectifs/form.html', {
        'form':  form,
        'titre': 'Nouvel objectif',
    })


@login_required
def objectif_modifier(request, pk):
    objectif = get_object_or_404(Objectif, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ObjectifForm(request.POST, instance=objectif)
        if form.is_valid():
            form.save()
            messages.success(request, "Objectif modifié avec succès !")
            return redirect('objectif_liste')
    else:
        form = ObjectifForm(instance=objectif)

    return render(request, 'objectifs/form.html', {
        'form':  form,
        'titre': 'Modifier l\'objectif',
    })


@login_required
def objectif_supprimer(request, pk):
    objectif = get_object_or_404(Objectif, pk=pk, user=request.user)

    if request.method == 'POST':
        objectif.delete()
        messages.success(request, "Objectif supprimé.")
        return redirect('objectif_liste')

    return render(request, 'objectifs/confirm_delete.html', {
        'objet': objectif,
        'titre': 'Supprimer l\'objectif',
        'message': f'Voulez-vous vraiment supprimer l\'objectif "{objectif.nom}" ?',
        'retour': 'objectif_liste',
    })


# ═══════════════════════════════════════════════════════
#  BUDGETS
# ═══════════════════════════════════════════════════════

@login_required
def budget_liste(request):
    today = date.today()
    budgets = Budget.objects.filter(user=request.user).select_related('categorie')

    budgets_data = []
    for budget in budgets:
        # Dépenses réelles pour cette catégorie ce mois
        depense_reelle = Transaction.objects.filter(
            user=request.user,
            type='depense',
            categorie=budget.categorie,
            date__month=budget.periode.month,
            date__year=budget.periode.year,
        ).aggregate(total=Sum('montant'))['total'] or 0

        if budget.montant_limite > 0:
            pourcentage = min(int((float(depense_reelle) / float(budget.montant_limite)) * 100), 100)
        else:
            pourcentage = 0

        # Couleur barre
        if pourcentage >= 100:
            couleur = 'danger'
        elif pourcentage >= 75:
            couleur = 'warning'
        else:
            couleur = 'success'

        budgets_data.append({
            'budget':        budget,
            'depense_reelle': depense_reelle,
            'pourcentage':   pourcentage,
            'couleur':       couleur,
            'restant':       float(budget.montant_limite) - float(depense_reelle),
            'depasse':       float(depense_reelle) > float(budget.montant_limite),
        })

    return render(request, 'budgets/liste.html', {
        'budgets_data': budgets_data,
    })


@login_required
def budget_ajouter(request):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget ajouté avec succès !")
            return redirect('budget_liste')
    else:
        form = BudgetForm(request.user)

    return render(request, 'budgets/form.html', {
        'form':  form,
        'titre': 'Nouveau budget',
    })


@login_required
def budget_modifier(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget modifié avec succès !")
            return redirect('budget_liste')
    else:
        form = BudgetForm(request.user, instance=budget)

    return render(request, 'budgets/form.html', {
        'form':  form,
        'titre': 'Modifier le budget',
    })


@login_required
def budget_supprimer(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget supprimé.")
        return redirect('budget_liste')

    return render(request, 'budgets/confirm_delete.html', {
        'objet':   budget,
        'titre':   'Supprimer le budget',
        'message': f'Voulez-vous vraiment supprimer le budget "{budget.categorie.nom}" ?',
        'retour':  'budget_liste',
    })