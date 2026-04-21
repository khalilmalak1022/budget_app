from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from .models import Budget, Transaction
from .forms_objectifs import BudgetForm


@login_required
def budget_liste(request):
    today = date.today()
    budgets = Budget.objects.filter(user=request.user).select_related('categorie')

    budgets_data = []
    for budget in budgets:
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

        if pourcentage >= 100:
            couleur = 'danger'
        elif pourcentage >= 75:
            couleur = 'warning'
        else:
            couleur = 'success'

        budgets_data.append({
            'budget':         budget,
            'depense_reelle': depense_reelle,
            'pourcentage':    pourcentage,
            'couleur':        couleur,
            'restant':        float(budget.montant_limite) - float(depense_reelle),
            'depasse':        float(depense_reelle) > float(budget.montant_limite),
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