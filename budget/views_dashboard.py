from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from collections import defaultdict
from .models import Transaction, Budget, Notification

@login_required
def dashboard(request):
    today = date.today()
    mois_actuel = today.month
    annee_actuelle = today.year

    # ─── Transactions du mois actuel ───────────────────────────────────────────
    transactions_mois = Transaction.objects.filter(
        user=request.user,
        date__month=mois_actuel,
        date__year=annee_actuelle
    )

    total_revenus = transactions_mois.filter(type='revenu').aggregate(
        total=Sum('montant'))['total'] or 0

    total_depenses = transactions_mois.filter(type='depense').aggregate(
        total=Sum('montant'))['total'] or 0

    solde = total_revenus - total_depenses

    # ─── Données camembert : dépenses par catégorie (mois actuel) ──────────────
    depenses_par_categorie = (
        transactions_mois
        .filter(type='depense')
        .values('categorie__nom', 'categorie__couleur')
        .annotate(total=Sum('montant'))
        .order_by('-total')
    )

    labels_camembert  = [d['categorie__nom']    or 'Sans catégorie' for d in depenses_par_categorie]
    valeurs_camembert = [float(d['total'])                          for d in depenses_par_categorie]
    couleurs_camembert= [d['categorie__couleur'] or '#cccccc'       for d in depenses_par_categorie]

    # ─── Données barres : revenus vs dépenses sur les 6 derniers mois ──────────
    labels_barres   = []
    revenus_barres  = []
    depenses_barres = []

    for i in range(5, -1, -1):
        # calcul du mois i mois en arrière
        m = mois_actuel - i
        a = annee_actuelle
        while m <= 0:
            m += 12
            a -= 1

        MOIS_FR = ['Jan','Fév','Mar','Avr','Mai','Jun',
                   'Jul','Aoû','Sep','Oct','Nov','Déc']
        labels_barres.append(f"{MOIS_FR[m-1]} {a}")

        qs = Transaction.objects.filter(user=request.user, date__month=m, date__year=a)
        rev = qs.filter(type='revenu' ).aggregate(t=Sum('montant'))['t'] or 0
        dep = qs.filter(type='depense').aggregate(t=Sum('montant'))['t'] or 0
        revenus_barres.append(float(rev))
        depenses_barres.append(float(dep))

    # ─── Alertes budgets dépassés ───────────────────────────────────────────────
    budgets_mois = Budget.objects.filter(
        user=request.user,
        periode__month=mois_actuel,
        periode__year=annee_actuelle
    ).select_related('categorie')

    alertes = []
    for budget in budgets_mois:
        depense_cat = transactions_mois.filter(
            type='depense',
            categorie=budget.categorie
        ).aggregate(total=Sum('montant'))['total'] or 0

        if depense_cat > budget.montant_limite:
            alertes.append({
                'categorie': budget.categorie.nom,
                'limite':    float(budget.montant_limite),
                'depense':   float(depense_cat),
                'depassement': float(depense_cat - budget.montant_limite),
            })

    # ─── Notifications non lues ─────────────────────────────────────────────────
    notifications_non_lues = Notification.objects.filter(
        user=request.user,
        est_lue=False
    ).count()

    # ─── Dernières transactions (5) ─────────────────────────────────────────────
    dernieres_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')[:5]

    # ─── Comparaison mois précédent ─────────────────────────────────────────────
    mois_prec = mois_actuel - 1 if mois_actuel > 1 else 12
    annee_prec = annee_actuelle if mois_actuel > 1 else annee_actuelle - 1

    depenses_mois_prec = Transaction.objects.filter(
        user=request.user,
        type='depense',
        date__month=mois_prec,
        date__year=annee_prec
    ).aggregate(total=Sum('montant'))['total'] or 0

    if depenses_mois_prec > 0:
        variation = ((total_depenses - depenses_mois_prec) / depenses_mois_prec) * 100
    else:
        variation = 0

    context = {
        # solde
        'total_revenus':   total_revenus,
        'total_depenses':  total_depenses,
        'solde':           solde,
        # camembert
        'labels_camembert':   labels_camembert,
        'valeurs_camembert':  valeurs_camembert,
        'couleurs_camembert': couleurs_camembert,
        # barres
        'labels_barres':    labels_barres,
        'revenus_barres':   revenus_barres,
        'depenses_barres':  depenses_barres,
        # alertes & notifs
        'alertes':                  alertes,
        'notifications_non_lues':   notifications_non_lues,
        # dernières transactions
        'dernieres_transactions':   dernieres_transactions,
        # comparaison
        'variation_depenses':       round(variation, 1),
        'depenses_mois_prec':       depenses_mois_prec,
        # date
        'mois_actuel': today.strftime('%B %Y'),
    }

    return render(request, 'dashboard.html', context)